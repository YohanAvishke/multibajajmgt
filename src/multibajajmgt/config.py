import logging

LOG_LEVEL = "WARNING"


def configure_logging():
    level = LOG_LEVEL
    if level == "DEBUG":
        # log level:logged message:full module path:function invoked:line number of logging call
        log_format = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
        logging.basicConfig(level = level, format = log_format)
    else:
        logging.basicConfig(level = level)
