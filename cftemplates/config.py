import os
from configparser import ConfigParser

from pkg_resources import resource_filename

config_parser = ConfigParser()
config_parser.read([resource_filename(__name__, 'defaults.ini'),
                    os.path.expanduser('~/.cftemplates/config.ini')])

def value(section, name):
    """
    Retrieve configuration setting

    :param section: Configuration setting section
    :param name: Configuration setting name
    :return: String, the value for the configuration setting
    """
    return config_parser.get(section, name)


