import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter

from src.utils.singleton import SingletonMeta


class Logger(metaclass=SingletonMeta):
    LOG_FORMAT_FOR_CMD = '%(log_color)s %(levelname)s:  %(log_color)s%(message)s%(reset)s'
    LOG_FORMAT_FOR_FILE = '%(asctime)s [%(levelname)s]: %(message)s'

    _logger = None
    _file_handler = None
    _stream_handler = None

    @staticmethod
    def __init_logger(output_dir=os.getcwd()):
        if Logger._logger is not None:
            return

        Logger._logger = logging.getLogger('autotests') 
        Logger._logger.setLevel(logging.INFO)
        Logger._logger.propagate = False

        Logger._stream_handler = logging.StreamHandler()
        Logger._stream_handler.setLevel(logging.INFO)
        Logger._stream_handler.setFormatter(ColoredFormatter(Logger.LOG_FORMAT_FOR_CMD))
        Logger._logger.addHandler(Logger._stream_handler)

        output_dir = os.path.join(output_dir, 'logs')
        os.makedirs(output_dir, exist_ok=True)

        file_path = f'{output_dir}/{datetime.now().strftime("%Y_%m_%d-%H_%M")}.log'
        Logger._file_handler = logging.FileHandler(file_path, 'w', 'utf-8')
        Logger._file_handler.setLevel(logging.INFO)
        Logger._file_handler.setFormatter(logging.Formatter(Logger.LOG_FORMAT_FOR_FILE))
        Logger._logger.addHandler(Logger._file_handler)

    @staticmethod
    def info(message):
        Logger.__init_logger()
        Logger._logger.info(message)

    @staticmethod
    def debug(message):
        Logger.__init_logger()
        Logger._logger.debug(message)

    @staticmethod
    def warn(message):
        Logger.__init_logger()
        Logger._logger.warning(message)

    @staticmethod
    def error_and_throw(message, exception_type=Exception):
        Logger.__init_logger()
        Logger._logger.error(message)
        raise exception_type(message)