import logging
from os import path
from os.path import isfile

from clink.iface import IErrorHandler
from clink.etc import LOGFILE_MODE
from clink.shell import touch
from clink.com.type import Component
from clink.com.marker import com
from clink.type import AppConf


@com(AppConf)
class ErrorLogHandler(Component, IErrorHandler):
    def __init__(self, app_conf):
        file = path.join('/var/tmp', app_conf.name, 'error.log')
        if not isfile(file):
            touch(file, LOGFILE_MODE)

        self._logger = logging.getLogger(file)
        fhandler = logging.FileHandler(file)
        formatter = logging.Formatter('%(asctime)s$ %(message)s')
        fhandler.setFormatter(formatter)
        self._logger.addHandler(fhandler)
        self._logger.setLevel(logging.INFO)

    def handle(self, req, res, e):
        msg = ' '.join([
            str(res.status), req.remote_addr, req.method, req.path,
            type(e).__name__
        ])
        self._logger.info(msg)
        return True
