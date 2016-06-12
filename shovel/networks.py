from configparser import ConfigParser as cp

from shovel import task


@task
def update_network_config():
    def current_config():
        config = cp()
        config.read([resource_filename(__name__, '../networks.ini'),
                     os.path.expanduser('~/.cftemplates/networks.ini')])
        return config.sections()