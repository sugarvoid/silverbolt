import logging

_filename = "silverbolt.log"

class Logger:
    """
    A wrapper for the built in logging package.

    """
    
    logging.basicConfig(filename=_filename, level=logging.INFO,format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


    @staticmethod
    def info(msg: str):
        logging.info(msg)
    
    @staticmethod
    def debug(mes: str):
        logging.debug(mes)

    @staticmethod
    def warning(mes: str):
        logging.warning(mes)
    
    @staticmethod
    def error(msg: str):
        logging.error(msg)
    
    @staticmethod
    def critical(mes: str):
        logging.critical(mes)

    @staticmethod
    def get_file_path():
        return _filename