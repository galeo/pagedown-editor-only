# -*- coding: utf-8 -*-

"""
Markdown content preview.

Convert Markdown content to HTML.

The original code is from
https://github.com/freedomsponsors/www.freedomsponsors.org/issues/4,
modified by galeo.
"""

import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
# from pygments import lexers, formatters
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class HighlighterRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        s = ''
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            s = '<div class="highlight"><span class="err">'\
                'Error: language "%s" is not supported</span></div>' % lang
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter()
        return ''.join([s, highlight(text, lexer, formatter)])

    def table(self, header, body):
        return ''.join(['<table class="table">\n',
                        header, '\n', body, '\n</table>'])

# And use the renderer
renderer = HighlighterRenderer(flags=misaka.HTML_SAFELINK |
                               misaka.HTML_SKIP_HTML)
md = misaka.Markdown(renderer,
                     extensions=misaka.EXT_FENCED_CODE |
                     misaka.EXT_NO_INTRA_EMPHASIS |
                     misaka.EXT_TABLES |
                     misaka.EXT_AUTOLINK |
                     misaka.EXT_SPACE_HEADERS |
                     misaka.EXT_STRIKETHROUGH |
                     misaka.EXT_SUPERSCRIPT)


def markdown(text):
    return md.render(text)
