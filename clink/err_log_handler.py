import logging
from os.path import isfile

from .ihandler import IErrorHandler
from .logging import LOGFILE_MODE
from .shell import touch


class ErrorLogHandler(IErrorHandler):
    def __init__(self, file):
        self._file = file

        if not isfile(file):
            touch(file, LOGFILE_MODE)

        self._logger = logging.getLogger(file)
        fhandler = logging.FileHandler(file)
        formatter = logging.Formatter('%(asctime)s$ %(message)s')
        fhandler.setFormatter(formatter)
        self._logger.addHandler(fhandler)
        self._logger.setLevel(logging.INFO)

    @property
    def file(self):
        return self._file

    def handle(self, req, res, e):
        msg = ' '.join([
            str(res.status), req.remote_addr, req.method, req.path,
            type(e).__name__
        ])
        self._logger.info(msg)
        return True
