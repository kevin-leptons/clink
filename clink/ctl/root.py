from clink import stamp, mapper, Controller, AppConf


@stamp(AppConf)
@mapper.path('/')
class RootCtl(Controller):
    '''
    APIs information
    '''

    def __init__(self, app_conf):
        self._info = {
            'name': app_conf.name,
            'license': app_conf.license,
            'version': str(app_conf.version),
            'organization': app_conf.org_name,
            'headquater': app_conf.org_addr
        }

    @mapper.get('/')
    def api_info(self, req, res):
        res.body = self._info
