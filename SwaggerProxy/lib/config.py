from __future__ import with_statement, absolute_import

import os.path

from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .errors import ConfigurationFileInitialized, ConfigurationFileNotFound


class ConfigBase(object):
    def __init__(self, config_file_path):
        self.options = load(open(config_file_path))


class Config(ConfigBase):
    def __init__(self, config_file_path, generate_if_not_found=True):
        if not os.path.isfile(config_file_path):
            if generate_if_not_found:
                self.reset_configfile(config_file_path)
            if os.path.isfile(config_file_path):
                raise ConfigurationFileInitialized("""No configuration file found.
A new file has been initialized at: %s
Please review the configuration and retry...""" % config_file_path)
            else:
                raise ConfigurationFileNotFound("cannot load config file %s" % config_file_path)

        super(Config, self).__init__(config_file_path)

    def reset_configfile(self, file_path):
        with open(file_path, 'w') as f:
            f.write(CONFIG_TEMPLATE)

CONFIG_TEMPLATE = """proxy:
 hostname: localhost
 port: 8000
api:
 url: http://localhost:8090/
swagger:
 file: ./core.yaml
"""