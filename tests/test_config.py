from cftemplates import config


def test_config():
    assert config.value('network', 'range') == '172.16.0.0'
