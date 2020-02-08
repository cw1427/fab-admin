"""
Created on 2018-2-11

@author: chenwen9
"""

import logging
import platform


class Logging(object):
    """Configure flask logging with nice formatting and syslog support."""

    def __init__(self, app=None, handler=None):
        """Boiler plate extension init with log_level being declared."""
        self.log_level = None
        self.app = app
        # Set up format for default logging
        hostname = platform.node().split('.')[0]
        self.formatter = (
            '[%(asctime)s] %(levelname)s %(process)d [%(name)s] '
            '%(filename)s:%(lineno)d - '
            '[{hostname}] - %(message)s'
        ).format(hostname=hostname)
        if app is not None:
            self.init_app(app, handler)

    def init_app(self, app, handler=None):
        """Setup the logging handlers, level and formatters.

        Level (DEBUG, INFO, CRITICAL, etc) is determined by the
        app.config['FLASK_LOG_LEVEL'] setting, and defaults to
        ``None``/``logging.NOTSET``.

        """
        config_log_level = app.config.get('LOG_LEVEL', None)
        config_log_int = None
        set_level = None

        if config_log_level:
            config_log_int = getattr(logging, config_log_level.upper(), None)
            if not isinstance(config_log_int, int):
                raise ValueError(
                    'Invalid log level: {0}'.format(config_log_level)
                )
            set_level = config_log_int

        # Set to NotSet if we still aren't set yet
        if not set_level:
            set_level = config_log_int = logging.NOTSET
        self.log_level = set_level

        # Setup basic StreamHandler logging with format and level (do
        # setup in case we are main, or change root logger if we aren't.
        logging.basicConfig(format=self.formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(set_level)
        bsm_logger = logging.getLogger(app.config.get('LOG_NAME', 'bsm'))
        bsm_logger.setLevel(set_level)
        if handler:
            bsm_logger.addHandler(handler)
        self.set_formatter(root_logger, self.formatter)
        self.set_formatter(bsm_logger, self.formatter)
        return config_log_int

    @staticmethod
    def set_formatter(logger, log_formatter):
        """Override the default log formatter with your own."""
        # Add our formatter to all the handlers
        for handler in logger.handlers:
            handler.setFormatter(logging.Formatter(log_formatter))

    def add_handler(self, handler):
        """inner method to add logger handler."""
        root_logger = self.app.logger
        handler.setFormatter(logging.Formatter(self.formatter))
        root_logger.addHandler(handler)
