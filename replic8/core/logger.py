import logging
import sys


class LoggerFactory:

    @classmethod
    def getDevLogger(cls):
        formatter = logging.Formatter(
            '%(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger = logging.getLogger('devLogger')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    @classmethod
    def getProdLogger(cls, path):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger = logging.getLogger('prodLogger')
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    @classmethod
    def getRootLogger(cls):
        return logging.getLogger('')
