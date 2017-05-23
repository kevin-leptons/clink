from clink.type.com import Service
from clink.com import stamp
from clink import AppConf, AuthConf


@stamp(AppConf, AuthConf)
class TemplateSv(Service):
    def __init__(self, app_conf, auth_conf):
        self._app_conf = app_conf
        self._auth_conf = auth_conf

    def build_file(file_path, values):
        # it should implement base on string.Template
        f = open(file_path)
        data = f.read()
        f.close()

        for k, v in values.items():
            data = data.replace(k, v)

        return data
