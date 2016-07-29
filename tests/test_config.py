from cftemplates import config


def test_config():
    """
    Test cftemplates.config.value
    """
    assert config.value('network', 'range') == '172.16.0.0'
