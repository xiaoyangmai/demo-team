import importlib.util
import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

from PIL import Image
import pytest

from harness.dspy_project import grade, inspect_artifact


@pytest.fixture
def comic(tmp_path):
    folder = tmp_path / 'artifacts'
    folder.mkdir()
    lesson = {'title': '一起试试', 'age_range': '6–8', 'learning_goal': '观察',
              'pages': [], 'questions': [], 'takeaway': '看清变化再判断。', 'practice': '和家人比较两片叶子的形状。'}
    for i, color in enumerate(('red', 'blue', 'green', 'orange'), 1):
        Image.new('RGB', (512, 512), color).save(folder / f'page-{i:02d}.png')
        lesson['pages'].append({'image': f'page-{i:02d}.png', 'alt': f'测试图{i}', 'caption': f'我们看到第{i}次变化。'})
    for i in (1, 2):
        lesson['questions'].append({'id': f'q{i}', 'prompt': '哪个发生了变化？', 'answer': 'B',
            'options': [{'id': k, 'text': v, 'feedback': '看看形状。' if k != 'B' else '对，形状变了。'}
                        for k, v in zip(('A','B','C'), ('颜色', '形状', '位置'))]})
    (folder / 'lesson.json').write_text(json.dumps(lesson, ensure_ascii=False), encoding='utf-8')
    script = Path(__file__).parents[1] / 'profiles/frontend/skills/illustrated-comic-delivery/scripts/render.py'
    spec = importlib.util.spec_from_file_location('comic_renderer', script)
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    renderer.render(folder)
    return tmp_path, lesson


def test_offline_reader_reaches_completion_and_resets(comic):
    folder, lesson = comic
    observed, images, checks = inspect_artifact(folder)
    assert observed == lesson and len(images) == 4
    assert len(checks['interactions']) == 12
    assert checks['completion_reached'] and checks['reset_verified'] and checks['offline']
    assert not any(q['conspicuous_length_cue'] for q in checks['answer_cues'])
    manifest = json.loads((folder / 'artifacts/manifest.json').read_text())
    assert len(manifest['artifacts']) == 6


def test_repeated_or_missing_illustrations_are_rejected(comic):
    folder, _ = comic
    target = folder / 'artifacts/page-04.png'
    target.write_bytes((folder / 'artifacts/page-01.png').read_bytes())
    with pytest.raises(AssertionError, match='identical image bytes'):
        inspect_artifact(folder)
    target.unlink()
    with pytest.raises(FileNotFoundError):
        inspect_artifact(folder)


def test_reader_must_show_each_declared_page_image(comic):
    folder, _ = comic
    path = folder / 'artifacts/index.html'
    html = path.read_text(encoding='utf-8')
    assert "$('art').src=p.image" in html
    path.write_text(html.replace("$('art').src=p.image", "$('art').src=lesson.pages[0].image"), encoding='utf-8')
    with pytest.raises(AssertionError, match='Displayed image differs'):
        inspect_artifact(folder)


def test_incomplete_comic_returns_actionable_feedback_without_model_grading(comic):
    folder, lesson = comic
    lesson['pages'] = lesson['pages'][:2]
    (folder / 'artifacts/lesson.json').write_text(json.dumps(lesson), encoding='utf-8')
    (folder / 'trace.json').write_text('[]', encoding='utf-8')
    result = grade(folder, {'topic': '观察'}, None)
    assert result['score'] == 0 and not result['deterministic']
    assert result['dimensions'] == {}
    assert 'Expected 4 illustrated pages; found 2' in result['feedback']


def test_judges_observe_independently_and_budget_does_not_hide_quality(comic, monkeypatch):
    import harness.dspy_project as project
    folder, lesson = comic
    rows = [{'tool_calls': [{'function': {'name': 'image_generate', 'arguments': '{}'}} for _ in range(6)]}]
    rows += [{'role': 'tool', 'tool_name': name, 'content': json.dumps({'success': True})}
             for name in ['image_generate'] * 4 + ['vision_analyze']]
    (folder / 'trace.json').write_text(json.dumps(rows), encoding='utf-8')
    checks = {'reading_lengths': {'captions': [], 'options': [], 'prompts': [], 'feedback': [], 'ending': []},
              'answer_cues': []}
    monkeypatch.setattr(project, 'inspect_artifact', lambda _: (lesson, [], checks))
    monkeypatch.setattr(project.dspy.Image, 'from_path', lambda path: path)
    monkeypatch.setattr(project.dspy, 'context', lambda **_: nullcontext())
    calls = []
    def predict(signature):
        assert signature is project.Assess
        def run(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(**{k: 3 for k in project.DIMENSIONS}, hard_fail=False,
                                   observations='visible observation', evidence='page evidence')
        return run
    monkeypatch.setattr(project.dspy, 'Predict', predict)
    result = grade(folder, {'topic': '观察'}, None)
    assert len(calls) == 2 and all('reader_observations' not in call for call in calls)
    assert result['score'] == result['quality_score'] == 0.75
    assert not result['budget_passed'] and not result['passed']
    assert len(result['judges']) == 2 and all(j['observations'] for j in result['judges'])
    rows[0]['tool_calls'] = rows[0]['tool_calls'][:4]
    (folder / 'trace.json').write_text(json.dumps(rows[:-1]), encoding='utf-8')
    result = grade(folder, {'topic': '观察'}, None)
    assert result['budget_passed'] and not result['process_passed'] and not result['passed']
    (folder / 'trace.json').write_text(json.dumps(rows), encoding='utf-8')
    assert grade(folder, {'topic': '观察'}, None)['passed']
