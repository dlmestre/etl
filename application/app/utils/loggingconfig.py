import logging
import logging.config
import yaml
import pkg_resources
import graypy

LOG_FILE = pkg_resources.resource_filename(__name__, '../config/logging.yaml')


class LogConfiguration:

    @staticmethod
    def set_logging():
        with open(LOG_FILE) as _log_file:
            logging.config.dictConfig(yaml.safe_load(_log_file))
        logging.getLogger()
