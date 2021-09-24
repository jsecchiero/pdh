from pdh import config
import tempfile
from yaml.scanner import ScannerError

VALID_YAML = """apikey: my_api_key
email: this_is_email
uid: USER_ID"""

BROKEN_YAML = """apikey: my_api_key
this is = broken
"""


def test_load_yaml_valid():
    fname = tempfile.mktemp()
    with open(fname, "w") as f:
        f.write(VALID_YAML)
        f.close()

    cfg = config.load_yaml(fname)
    assert cfg != {}
    assert "apikey" in cfg
    assert "email" in cfg
    assert "uid" in cfg
    assert cfg["apikey"] == "my_api_key"
    assert cfg["email"] == "this_is_email"
    assert cfg["uid"] == "USER_ID"


def test_load_yaml_broken():
    fname = tempfile.mktemp()
    with open(fname, "w") as f:
        f.write(BROKEN_YAML)
        f.close()

    try:
        _ = config.load_yaml(fname)
    except ScannerError:
        assert True
        return
    assert False


def test_save_yaml():
    cfg = {"a": 1, "b": 2, "c": {"d": 3}}
    fname = tempfile.mktemp()
    r = config.save_yaml(fname, cfg)
    assert r


def test_not_valid_config():
    cfg = {"a": 1, "b": 2, "c": {"d": 3}}
    assert config.valid_config(cfg) is False


def test_load_and_validate():
    fname = tempfile.mktemp()
    with open(fname, "w") as f:
        f.write(VALID_YAML)
        f.close()

    cfg = config.load_and_validate(fname)
    assert cfg != {}
