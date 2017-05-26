from clink import stamp, mapper, Controller, AppConf


@stamp(AppConf)
@mapper.path('')
class RootCtl(Controller):
    def __init__(self, app_conf):
        self._app_conf = app_conf

    @mapper.get('')
    def api_info(self, req, res):
        res.body = {
            'name': self._app_conf.name,
            'license': self._app_conf.license,
            'version': str(self._app_conf.version),
            'organization': self._app_conf.org_name,
            'headquater': self._app_conf.org_addr
        }
