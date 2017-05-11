import logging
from os.path import isfile

from .logging import LOGFILE_MODE, LOGFILE_ERR
from .shell import touch

if not isfile(LOGFILE_ERR):
    touch(LOGFILE_ERR, LOGFILE_MODE)

_logger = logging.getLogger('clink-error')
_fhandler = logging.FileHandler(LOGFILE_ERR)
_formatter = logging.Formatter('%(asctime)s$ %(message)s')
_fhandler.setFormatter(_formatter)
_logger.addHandler(_fhandler)
_logger.setLevel(logging.INFO)


def log_err_handle(req, res, e):
    msg = ' '.join([
        str(res.status), req.remote_addr, req.method, req.path,
        type(e).__name__
    ])
    _logger.info(msg)
    return True
