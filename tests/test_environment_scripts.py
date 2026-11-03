import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml


PROJECT_ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize(('enabled', 'ready'), [(False, True), (True, False), ('false', False), (None, False)])
def test_environment_check_requires_curator_disabled(tmp_path, enabled, ready):
    profile = tmp_path / 'profiles' / 'frontend'
    profile.mkdir(parents=True)
    config = {'auxiliary': {'background_review': {'enabled': False}},
              'agent': {'disabled_toolsets': ['code_execution']}}
    if enabled is not None:
        config['curator'] = {'enabled': enabled}
    (profile / 'config.yaml').write_text(yaml.safe_dump(config), encoding='utf-8')
    source = (PROJECT_ROOT / 'ops' / 'check-environment').read_text(encoding='utf-8')
    code = source.split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    env = dict(os.environ, HERMES_HOME=str(tmp_path))
    process = subprocess.run([sys.executable, '-c', code], cwd=PROJECT_ROOT,
                             env=env, check=True, capture_output=True, text=True)
    details = json.loads(process.stdout)
    assert details['checks']['curator_disabled'] is ready
    assert details['ready'] is ready


def test_declared_profile_disables_curator():
    config = yaml.safe_load((PROJECT_ROOT / 'profiles' / 'frontend' / 'config.yaml').read_text(encoding='utf-8'))
    assert config['curator']['enabled'] is False
