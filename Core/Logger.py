import logging.config

class Logger:


    def __init__(self, tag):
        self.logger = logging.getLogger(tag)
        self.level = logging.DEBUG
        self.tag = tag
        fh = logging.FileHandler(tag + ".log")
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)

    def log(self, msg, lvl = None):
        if lvl is not None:
            self.level = lvl
