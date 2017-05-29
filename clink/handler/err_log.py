import logging
from os import path
from os.path import isfile
from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH

from clink.iface import ILv8Handler
from clink.util.shell import touch
from clink.com import stamp
from clink.type import AppConf

LOGFILE_MODE = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH


@stamp(AppConf)
class ErrorLogHandler(ILv8Handler):
    '''
    Catch error, write information to file at
    /var/tmp/<app-name>/error.log
    '''

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
