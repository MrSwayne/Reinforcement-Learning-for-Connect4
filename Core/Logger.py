import logging
from Core.Conf import *

class Logger:

    def __init__(self, filename):
        print("Logging to: ", filename)
        self._filename = filename
        self.loggers = {}

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, f):
        print("Logging to: ", f)
        self._filename = f

    def attach(self, name, filename = None):
        print("Attaching Logger: " + str(name))
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        if filename is None:
            fh = logging.FileHandler(self.filename + ".log")
        else:
            fh = logging.FileHandler(filename + ".log")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        self.loggers[name] = logger
        return logger

#IO.verify(cfg["IO"]["log_path"])
log_path = cfg["IO"]["log_path"] + cfg["LOGGING"].get("file_name", "log.out")
LOGGER = Logger(log_path)