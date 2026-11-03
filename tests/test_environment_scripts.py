import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml


PROJECT_ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize(('enabled', 'runtime_override', 'ready'),
                         [(False, False, True), (False, True, False), (True, False, False),
                          ('false', False, False), (None, False, False)])
def test_environment_check_requires_curator_disabled(tmp_path, enabled, runtime_override, ready):
    profile = tmp_path / 'profiles' / 'frontend'
    profile.mkdir(parents=True)
    config = {'auxiliary': {'background_review': {'enabled': False}},
              'agent': {'disabled_toolsets': ['code_execution']}}
    if enabled is not None:
        config['curator'] = {'enabled': enabled}
    (profile / 'config.yaml').write_text(yaml.safe_dump(config), encoding='utf-8')
    skills = profile / 'skills'
    skills.mkdir()
    (skills / '.curator_state').write_text('existing state', encoding='utf-8')
    (skills / 'SKILL.md').write_text('fixed skill', encoding='utf-8')
    fake_agent = tmp_path / 'imports' / 'agent'
    fake_agent.mkdir(parents=True)
    (fake_agent / '__init__.py').write_text('', encoding='utf-8')
    (fake_agent / 'curator.py').write_text(
        "import os, pathlib, yaml\n"
        "def is_enabled():\n"
        "    config = yaml.safe_load((pathlib.Path(os.environ['HERMES_HOME']) / 'config.yaml').read_text())\n"
        "    return os.environ['TEST_RUNTIME_ENABLED'] == '1' or bool(config.get('curator', {}).get('enabled', True))\n", encoding='utf-8')
    source = (PROJECT_ROOT / 'ops' / 'check-environment').read_text(encoding='utf-8')
    code = source.split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    env = dict(os.environ, HERMES_HOME=str(tmp_path), PYTHONPATH=str(fake_agent.parent),
               TEST_RUNTIME_ENABLED='1' if runtime_override else '0')
    process = subprocess.run([sys.executable, '-c', code], cwd=PROJECT_ROOT,
                             env=env, check=True, capture_output=True, text=True)
    details = json.loads(process.stdout)
    assert details['checks']['curator_disabled'] is ready
    assert details['ready'] is ready
    assert details['curator_disabled_profiles'] == ['frontend']
    files = {path.replace('\\', '/') for path in details['files']}
    assert ('skills/.curator_state' not in files) is ready
    assert 'skills/SKILL.md' in files


def test_declared_profile_disables_curator():
    config = yaml.safe_load((PROJECT_ROOT / 'profiles' / 'frontend' / 'config.yaml').read_text(encoding='utf-8'))
    assert config['curator']['enabled'] is False
