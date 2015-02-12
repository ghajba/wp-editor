from wpedit import configuration
import os


def data_dir():
    return os.path.join(os.path.dirname(__file__), 'mdxml.conf')


def test_configuration():
    config = configuration.Configuration()
    config.load_configuration(data_dir())

    assert len(config.get_normal()) == 3

    assert config.alter_multiline("~~~~~~~~"), "Multiline marker not working"

