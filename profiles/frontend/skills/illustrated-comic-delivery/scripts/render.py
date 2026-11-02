"""Package an authored lesson and four local illustrations; no model or network calls."""
import json
from pathlib import Path
import sys


def render(folder):
    lesson = json.loads((folder / 'lesson.json').read_text(encoding='utf-8'))
    data = json.dumps(lesson, ensure_ascii=False).replace('<', '\\u003c')
    template = Path(__file__).with_name('reader.html').read_text(encoding='utf-8')
    (folder / 'index.html').write_text(template.replace('__LESSON_DATA__', data), encoding='utf-8')
    artifacts = [{'path': 'index.html', 'name': 'index.html', 'kind': 'document', 'content_type': 'text/html'},
                 {'path': 'lesson.json', 'name': 'lesson.json', 'kind': 'data', 'content_type': 'application/json'}]
    for page in lesson['pages']:
        filename = page['image']
        mime = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}[Path(filename).suffix]
        artifacts.append({'path': filename, 'name': filename, 'kind': 'image', 'content_type': mime})
    (folder / 'manifest.json').write_text(json.dumps({'artifacts': artifacts}, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    render(Path(sys.argv[1]))
