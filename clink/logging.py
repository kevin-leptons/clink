from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH

LOGFILE_REQ = '/var/tmp/clink/request.log'
LOGFILE_RES = '/var/tmp/clink/response.log'
LOGFILE_ERR = '/var/tmp/clink/error.log'

LOGFILE_MODE = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH
