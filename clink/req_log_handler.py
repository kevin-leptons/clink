import logging
from os.path import isfile

from .logging import LOGFILE_MODE, LOGFILE_REQ
from .shell import touch

if not isfile(LOGFILE_REQ):
    touch(LOGFILE_REQ, LOGFILE_MODE)

_logger = logging.getLogger('clink-request')
_fhandler = logging.FileHandler(LOGFILE_REQ)
_formatter = logging.Formatter('%(asctime)s$ %(message)s')
_fhandler.setFormatter(_formatter)
_logger.addHandler(_fhandler)
_logger.setLevel(logging.INFO)


def log_req_handle(req, res):
    _logger.info('%s %s %s' % (req.remote_addr, req.method, req.path))
