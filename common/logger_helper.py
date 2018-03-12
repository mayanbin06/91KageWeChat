#encoding=utf-8
import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

default_log_file = './all.log'
default_error_log_file = './error.log'

def init_logger(logger_name, log_file = default_log_file, error_log_file = default_error_log_file):
    if logger_name not in Logger.manager.loggerDict:
        logger1 = logging.getLogger(logger_name)
        #logger1.setLevel(logging.INFO)  # 设置最低级别
        logger1.setLevel(logging.DEBUG)  # 设置最低级别
        df = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s'
        formatter = logging.Formatter(format_str, df)
        # handler all
        handler1 = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=7)
        handler1.setFormatter(formatter)
        handler1.setLevel(logging.DEBUG)
        logger1.addHandler(handler1)
        # handler error
        handler2 = TimedRotatingFileHandler(error_log_file, when='D', interval=1, backupCount=7)
        handler2.setFormatter(formatter)
        handler2.setLevel(logging.ERROR)
        logger1.addHandler(handler2)

        # console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)

        console.setFormatter(formatter)

        logger1.addHandler(console)

    logger1 = logging.getLogger(logger_name)
    return logger1

if __name__ == '__main__':
    logger = init_logger('runtime-log')
    logger.debug('test-debug')
    logger.info('test-info')
    logger.warn('test-warn')
    logger.error('test-error')