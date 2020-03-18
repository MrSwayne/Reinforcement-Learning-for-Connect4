import logging

class Logger:

    def __init__(self, filename):
        self.filename = filename
        self.loggers = {}

    def attach(self, name, filename = None):
        print("Attaching " + str(name))
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        if filename is None:
            fh = logging.FileHandler(self.filename + ".log")
        else:
            fh = logging.FileHandler(filename + ".log")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        self.loggers[name] = logger
        return logger

LOGGER = Logger("out")