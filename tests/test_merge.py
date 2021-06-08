import hashlib
import os
import pytest
import yaml

from pathlib import Path
from env_config import merge_config_files_from_envvars

EXPECTED_RESULT = Path(__file__).parent.parent.joinpath('example', 'expected.yaml')
ACTUAL_RESULT = Path(__file__).parent.parent.joinpath('example', 'actual.yaml')


@pytest.fixture(scope='module', autouse=True)
def set_envvars():
    os.environ['MAIN_CONFIG_FILE'] = str(
        Path(__file__).parent.parent.joinpath('example', 'config_main.yaml')
    )
    os.environ['LOCAL_CONFIG_FILE'] = str(
        Path(__file__).parent.parent.joinpath('example', 'config_local.yaml')
    )
    os.environ['INVALID_PATH'] = str(
        Path(__file__).parent.parent.joinpath('example', 'config_invalid.yaml')
    )
    yield
    if ACTUAL_RESULT.exists():
        os.remove(ACTUAL_RESULT)
    if 'MAIN_CONFIG_FILE' in os.environ.keys(): os.environ.pop('MAIN_CONFIG_FILE')
    if 'LOCAL_CONFIG_FILE' in os.environ.keys(): os.environ.pop('LOCAL_CONFIG_FILE')
    if 'INVALID_PATH' in os.environ.keys():os.environ.pop('INVALID_PATH')


def files_identical(path1: Path, path2: Path) -> bool:
    """Compares content of file using md5 checksum"""
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        f1 = f1.read()
        f2 = f2.read()
    if hashlib.md5(f1).hexdigest() == hashlib.md5(f2).hexdigest():
        return True
    return False


def test_merge_two_yaml_files():
    result = merge_config_files_from_envvars(('MAIN_CONFIG_FILE', 'LOCAL_CONFIG_FILE', 'INVALID_PATH'))
    with open(ACTUAL_RESULT, 'x') as stream:
        yaml.safe_dump(result, stream=stream, sort_keys=False)
    assert files_identical(ACTUAL_RESULT, EXPECTED_RESULT)
