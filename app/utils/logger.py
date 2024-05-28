import logging
import logging.config
import logging.handlers


class Logger:
    @classmethod
    def get_daemon_logger(cls):
        return logging.getLogger("daemon")
