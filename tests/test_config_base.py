from libclamav_py.config.base import ConfigBase


def test_base():
    base = ConfigBase()
    assert base is not None


def test_base_to_bit_flag():
    base = ConfigBase()
    base._to_bit_flag()
