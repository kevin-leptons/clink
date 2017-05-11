import logging
from os.path import isfile

from .logging import LOGFILE_MODE, LOGFILE_RES
from .shell import touch

if not isfile(LOGFILE_RES):
    touch(LOGFILE_RES, LOGFILE_MODE)

_logger = logging.getLogger('clink-response')
_fhandler = logging.FileHandler(LOGFILE_RES)
_formatter = logging.Formatter('%(asctime)s$ %(message)s')
_fhandler.setFormatter(_formatter)
_logger.addHandler(_fhandler)
_logger.setLevel(logging.INFO)


def log_res_handle(req, res):
    _logger.info('%i %s %s' % (res.status, req.method, req.path))
