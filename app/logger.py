import logging

logging.basicConfig(filename='info.log', format='%(levelname)s:%(message)s', level=logging.INFO)


class Logger:
    @staticmethod
    def info(msg):
        print("INFO: %s" % msg)
        logging.info(msg)

    @staticmethod
    def debug(msg):
        print("DEBUG: %s" % msg)
        logging.debug(msg)

    @staticmethod
    def warn(msg):
        print("WARNING: %s" % msg)
        logging.warning(msg)

    @staticmethod
    def error(msg):
        print("ERROR: %s" % msg)
        logging.error(msg)