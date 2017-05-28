from sphinx.util.compat import Directive
from docutils import nodes


class text_msg(nodes.Element):
    pass


class TextMsgDirective(Directive):
    '''
    Write text message such as HTTP message
    '''

    has_content = True

    def run(self):
        node = nodes.literal_block()
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class TextMsgDivDirective(Directive):
    '''
    Write text message such as HTTP message
    '''

    has_content = True

    def run(self):
        node = nodes.literal_block(text='\n\n')
        return [node]
