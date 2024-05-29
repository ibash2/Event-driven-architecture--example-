import logging
import logging.config
import logging.handlers


daemon_logger = logging.getLogger("daemon")
consumer_logger = logging.getLogger("consumer")
order_logger = logging.getLogger("order")
# other logger
