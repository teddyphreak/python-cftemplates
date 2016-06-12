import os
from configparser import ConfigParser as cp

from pkg_resources import resource_filename

config_settings = cp()
config_settings.read([resource_filename(__name__, '../defaults.ini'),
                      os.path.expanduser('~/.cftemplates/config.ini')])


def value(section, name):
    return config_settings.get(section, name)


