import logging
from os.path import isfile

from ..etc import LOGFILE_MODE
from ..iface import IPipeHandler
from ..shell import touch


class ReqLogHandler(IPipeHandler):
    def __init__(self, file):
        self._file = file
        self.logger = logging.getLogger(file)

        if not isfile(file):
            touch(file, LOGFILE_MODE)

        fhandler = logging.FileHandler(file)
        formatter = logging.Formatter('%(asctime)s$ %(message)s')
        fhandler.setFormatter(formatter)
        self.logger.addHandler(fhandler)
        self.logger.setLevel(logging.INFO)

    @property
    def file(self):
        return self._file

    def handle(self, req, res, ctx):
        msg = '%s %s %s' % (req.remote_addr, req.method, req.path)
        self.logger.info(msg)
