import json
from contextlib import nullcontext
from types import SimpleNamespace

import harness.dspy_project as project
import pytest
from harness.dspy_project import decide, environment_report, task, trace_summary, DIMENSIONS


def grade(scores, passed=True):
    value = 0.6 * min(scores) / 4 + 0.4 * sum(scores) / (4 * len(scores))
    return {"case_id": "case", "score": value, 'quality_score': value, "passed": passed,
            "dimensions": dict(zip(DIMENSIONS, scores))}


def test_average_gain_cannot_hide_regression():
    result = decide({"baseline": [grade([3, 3, 3, 4, 3, 3])], "candidate": [grade([4, 4, 4, 3, 4, 4])]})
    assert result["mean_gain"] > 0
    assert not result["adopt"] and result["regressed_cases"] == [0]


def test_real_gain_without_regression_can_be_adopted():
    assert decide({"baseline": [grade([3]*6)], "candidate": [grade([4, 4, 3, 3, 3, 3])]})["adopt"]


def test_failed_candidate_and_equal_score_are_not_promoted():
    assert not decide({"baseline": [grade([3]*6)], "candidate": [grade([4]*6, False)]})["adopt"]
    assert not decide({"baseline": [grade([3]*6)], "candidate": [grade([3]*6)]})["adopt"]


def test_environment_contract_matches_control_plane():
    details = {"ready": True, "revision": "sha", "files": {"SOUL.md": "hash"}}
    assert environment_report({"ready": True, "check": {"ready": True, "details": details}}) == details


def test_budget_compliance_alone_is_not_an_artifact_quality_gain():
    baseline = grade([3]*6, False)
    baseline['score'] = 0
    decision = decide({'baseline': [baseline], 'candidate': [grade([3]*6)]})
    assert decision['mean_gain'] > 0 and decision['quality_mean_gain'] == 0
    assert not decision['adopt']


def test_incomplete_or_mismatched_comparison_cannot_be_adopted():
    a, b = grade([3]*6), grade([4]*6)
    with pytest.raises(ValueError, match='complete and paired'):
        decide({'baseline': [a, a], 'candidate': [b]})
    b['case_id'] = 'different'
    with pytest.raises(ValueError, match='complete and paired'):
        decide({'baseline': [a], 'candidate': [b]})


def test_image_budget_counts_native_and_deferred_calls_not_rejected_batches():
    def call(name, args):
        return {'function': {'name': name, 'arguments': json.dumps(args)}}
    image = {'name': 'image_generate', 'arguments': {'prompt': 'page ' * 400}}
    rows = [{'tool_calls': [call('image_generate', {'prompt':'page'}),
                          call('tool_call', {'calls':[image]}),
                          call('tool_call', {'calls':[image,image]}),
                          call('vision_analyze', {'image_url':'page.jpg'})]}]
    summary = trace_summary(rows)
    assert summary['image_generation_attempts'] == 2
    assert [c['arguments_truncated'] for c in summary['tool_calls']] == [False, True, True, False]
    assert len(summary['tool_calls'][1]['arguments']) == 1500


def test_task_uses_experiment_workspace():
    request = task({'topic': '分类'}, 'sample', 'abc', '/opt/data/experiments/a/projects/demo-team')
    assert '/opt/data/experiments/a/projects/demo-team' in request['instructions']


def test_visual_calibration_checks_both_real_judges_and_failure_blocks(monkeypatch):
    monkeypatch.setattr(project.dspy, 'context', lambda **_: nullcontext())
    monkeypatch.setattr(project.dspy.Image, 'from_path', lambda path: path)
    calls = []
    def predict(_):
        def run(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(**{name: 3 for name in DIMENSIONS}, hard_fail=False, observations='seen', evidence='page')
        return run
    monkeypatch.setattr(project.dspy, 'Predict', predict)
    result = project.calibrate(None)
    assert not result['passed']
    visual = [call for call in calls if call['pictures']]
    assert len(visual) == 14 and all(call['pictures'][0].endswith('bridge.jpg') for call in visual)
    assert len([item for item in result['controls'] if item['control'] == 'contradictory_state' and not item['passed']]) == 2
