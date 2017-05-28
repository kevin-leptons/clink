import json
from importlib import import_module
from sphinx.util.compat import Directive
from docutils import nodes


class JsonDumpDirective(Directive):
    '''
    Convert dictionary to json string, then insert into document
    '''

    has_content = True
    required_arguments = 1

    def run(self):
        coms = self.arguments[0].split('.')
        module_name = '.'.join(coms[:-1])
        var_name = coms[-1:][0]
        module = import_module(module_name)
        data = getattr(module, var_name)
        json_str = json.dumps(
            data, sort_keys=True, indent=4, separators=(',', ': ')
        )
        node = nodes.literal_block(text=json_str)
        return [node]
