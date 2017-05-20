import logging
from os import path
from os.path import isfile

from clink.etc import LOGFILE_MODE
from clink.iface import IPipeHandler
from clink.shell import touch
from clink.com.marker import com
from clink.type import Lv1Handler
from clink.type import AppConf


@com(AppConf)
class ReqLogHandler(Lv1Handler, IPipeHandler):
    def __init__(self, app_conf):
        file = path.join('/var/tmp', app_conf.name, 'request.log')
        if not isfile(file):
            touch(file, LOGFILE_MODE)

        self.logger = logging.getLogger(file)
        fhandler = logging.FileHandler(file)
        formatter = logging.Formatter('%(asctime)s$ %(message)s')
        fhandler.setFormatter(formatter)
        self.logger.addHandler(fhandler)
        self.logger.setLevel(logging.INFO)

    def handle(self, req, res):
        msg = '%s %s %s' % (req.remote_addr, req.method, req.path)
        self.logger.info(msg)
