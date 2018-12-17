import configparser
import os

import consul
import pkg_resources

import logging

log = logging.Logger(__name__)

CONSUL_SERVER = os.getenv('CONSUL_SERVER')
CONSUL_PATH = os.getenv('CONSUL_KEY')


class EnvInterpolation(configparser.BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


class OpsConfiguration:

    @staticmethod
    def set_config():
        config_parser = configparser.ConfigParser(interpolation=EnvInterpolation())
        if not OpsConfiguration._load_consul(config_parser):
            log.info('Running config file')
            config_file = pkg_resources.resource_filename(__name__, '../config/config.ini')
            config_parser.read(config_file)
        return config_parser

    @staticmethod
    def _load_consul(config_parser):
        if CONSUL_SERVER and CONSUL_PATH:
            log.info('Running consul')
            consul_server = consul.Consul(CONSUL_SERVER)
            _, consul_config = consul_server.kv.get(CONSUL_PATH)

            consul_configuration = consul_config['Value'].decode()
            config_parser.read_string(consul_configuration)
