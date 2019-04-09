import logging


class Mylogger(object):
    def __init__(self, filename=None, name=None, stream=True, format=None, level="debug"):
        self.logger = logging.getLogger(name) if name else logging.getLogger()

        try:
            if hasattr(logging, level.upper()):
                self.logger.setLevel(getattr(logging, level.upper()))
        except Exception as e:
            raise e


        if format:
            fmt = logging.Formatter(fmt=format)
        else:
            fmt = logging.Formatter(fmt='%(filename)s [%(lineno)s] %(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if filename:
            fh = logging.FileHandler(filename, mode="a", encoding="utf-8")
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)

        if stream:
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            self.logger.addHandler(sh)

    def getlogger(self):
        return self.logger


if __name__ == '__main__':
    logger = Mylogger(name="12306", filename="logger.log", level="debug", stream=True).getlogger()

    logger.warning("warning")
    logger.error("error")
    logger.info("info")
    logger.debug("debug")
    logger.critical("critical")