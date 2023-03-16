from pytest import raises

from edward.config import Ini, MissingFile


def test_not_able_to_init_without_config_file():
    message_error = "Missing config file, run with --config to configure"

    with raises(MissingFile) as error:
        Ini(filename="force_error.ini")

    assert error.value.args[0] == message_error
