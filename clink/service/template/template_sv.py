from string import Template
from datetime import datetime

from clink.type import AppConf, AuthConf, Service
from clink.com import stamp


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

        self._base_values = {
            'app_name': app_conf.name,
            'root_name': 'root',
            'root_email': auth_conf.root_email,
            'datetime_now': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }

    def build_file(self, file_path, values):
        '''
        Read data from file then build it as a template

        :param str file_path:
        :param dict values:
        :rtype: str
        '''

        f = open(file_path)
        data = f.read()
        f.close()

        return self.build_str(data, values)

    def build_str(self, data, values):
        '''
        Build string template

        :param str data:
        :param dict values:
        :rtype: str
        '''

        values.update(self._base_values)
        return Template(data).safe_substitute(values)
