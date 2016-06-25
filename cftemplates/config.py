import os
from configparser import ConfigParser

from pkg_resources import resource_filename

config_settings = ConfigParser()
config_settings.read([resource_filename(__name__, 'defaults.ini'),
                      os.path.expanduser('~/.cftemplates/config.ini')])


def value(section, name):
    return config_settings.get(section, name)


