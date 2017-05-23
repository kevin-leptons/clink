from string import Template

from clink.type.com import Service
from clink.com import stamp
from clink import AppConf, AuthConf


@stamp(AppConf, AuthConf)
class TemplateSv(Service):
    '''
    Simple template engine
    '''

    def __init__(self, app_conf, auth_conf):
        '''
        :param AppConf app_conf:
        :param AuthConf auth_conf:
        '''

        self._app_conf = app_conf
        self._auth_conf = auth_conf

    def build_file(file_path, values):
        '''
        Read data from file then build it as a template

        :param str file_path:
        :param dict values:
        :rtype: str
        '''
        
        f = open(file_path)
        data = f.read()
        f.close()

        return self.build_str(data)

    def build_str(self, data, values):
        '''
        Build string template

        :param str data:
        :param dict values:
        :rtype: str
        '''
        
        return Template(data).safe_substitute(values)
