# -*- coding: utf-8 -*-

# Markdown parsers.
#
#
# Author: Moogen Tian <http://blog.galeo.me>
#
# Legal:
#
#   This file is published under BSD License.
#
#     And the code structure references:
#
#       * pagewise (by ainm <ainm at gmx.com>, with personal public license)
#
#       * mynt (by Andrew Fricke, the author of Hoep, with BSD license)
#
#     please NOTICE that!
#

# Hoep only accepts and returns *unicode* objects in Python 2 and
# *str* objects in Python 3.
from __future__ import unicode_literals

import re
import sys


#
# Error handling.
#

class MDParserException(Exception):
    pass


def error(message, *args):
    """
    Raise a MDParserException with a given message.
    """
    raise MDParserException(message % args)


def warning(message, *args):
    """
    Just display a message to standard error.
    """
    sys.stderr.write("WARNING: " + message % args)


def halt(message, *args):
    """
    Display a message to standard error and stop the program.
    """
    sys.stderr.write("FATAL: " + message % args)
    sys.exit(1)


#
# Markup support.
#

# Tables with bootstrap
def tablestrap(content, class_=''):
    if class_:
        class_ = class_.split()
    if isinstance(class_, list):
        if 'table' not in class_:
            class_ = ['table'] + class_
        class_ = ' '.join(class_)
    if class_:
        class_ = 'class="%s"' % class_
    return ''.join(['<table ', class_, '>\n',
                    content, '\n</table>'])


# Pygments.

HAVE_PYGMENTS = True

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

except ImportError:
    HAVE_PYGMENTS = False


def require_pygments():
    """
    For error reporting when trying to use a markup language
    with pygments, but pygments isn't installed.
    """
    if not HAVE_PYGMENTS:
        error("please, install Pygments <http://pygments.org/>.")


def hl_with_pygments(text, lang, fmt_options={}):
    s = ''

    formatter = HtmlFormatter(**fmt_options)
    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except ValueError:
        s = '<div class="highlight"><span class="err">'\
            'Error: language "%s" is not supported</span></div>' % lang
        lexer = get_lexer_by_name('text', stripall=True)
    return ''.join([s, highlight(text, lexer, formatter)])


# Available renderers will add themselves to this hash.
# The key is the renderer name, the value is another hash
# with two keys/values, the renderer constructor/options.

MARKUP_RENDERERS = {}

def xlate_exts_flags(exts_flags_opts, parser_exts_flags):
    actual_exts = 0
    actual_flags = 0

    exts = exts_flags_opts['extensions']
    flags = exts_flags_opts['render_flags']

    parser_exts = parser_exts_flags['extensions']
    parser_flags = parser_exts_flags['render_flags']

    if ('fenced_code' in exts) or ('tables' in exts):
        require_pygments()

    for ext in exts:
        if ext in parser_exts:
            actual_exts |= parser_exts[ext]
        else:
            warning("ignoring unknown extension: %s", str(ext))

    for flag in flags:
        if flag in parser_flags:
            actual_flags |= parser_flags[flag]
        else:
            warning("ignoring unknown render flag: %s", str(flag))

    return actual_exts, actual_flags

#
# Misaka.
#

HAVE_MISAKA = True

try:
    import misaka
    from misaka import HtmlRenderer

    MISAKA_EXTS_FLAGS = {
        'extensions': {
            'tables':                misaka.EXT_TABLES,
            'fenced_code':           misaka.EXT_FENCED_CODE,
            'footnotes':             misaka.EXT_FOOTNOTES,
            'autolink':              misaka.EXT_AUTOLINK,
            'strikethrough':         misaka.EXT_STRIKETHROUGH,
            'underline':      	     misaka.EXT_UNDERLINE,
            'highlight':	         misaka.EXT_HIGHLIGHT,
            'quote':	             misaka.EXT_QUOTE,
            'superscript':           misaka.EXT_SUPERSCRIPT,
            'math':          	     misaka.EXT_MATH,
            'no_intra_emphasis':     misaka.EXT_NO_INTRA_EMPHASIS,
            'space_headers':         misaka.EXT_SPACE_HEADERS,
            'math_explicit':	     misaka.EXT_MATH_EXPLICIT,
            'disable_indented_code': misaka.EXT_DISABLE_INDENTED_CODE
        },
        'render_flags': {
            'skip_html': misaka.HTML_SKIP_HTML,
            'escape':    misaka.HTML_ESCAPE,
            'hard_wrap': misaka.HTML_HARD_WRAP,
            'use_xhtml': misaka.HTML_USE_XHTML,
        }
    }

    class MisakaRenderer(HtmlRenderer):
        def __init__(self, tbl_class='', fmt_options={}, *args, **kwargs):
            super(MisakaRenderer, self).__init__(*args, **kwargs)
            self.tbl_class = tbl_class
            self.fmt_options = fmt_options

        if HAVE_PYGMENTS:
            def blockcode(self, text, lang):
                return hl_with_pygments(text, lang, self.fmt_options)

        def table(self, content):
            return tablestrap(content, self.tbl_class)

    def misaka_renderer(options, tbl_class='', fmt_options={}):
        """
        Returns a function that can be used to transform Markdown to HTML
        using Misaka, preconfigured with the given extensions/flags.
        """
        Renderer = MisakaRenderer
        used_exts, used_flags = xlate_exts_flags(options, MISAKA_EXTS_FLAGS)
        return misaka.Markdown(Renderer(tbl_class, fmt_options, used_flags), used_exts)

    MARKUP_RENDERERS['misaka'] = {
        'renderer': misaka_renderer,
        'options':  ['extensions', 'render_flags'],
    }

except ImportError:
    HAVE_MISAKA = False


#
# hoep
#

HAVE_HOEP = True

try:
    import hoep as h

    HOEP_EXTS_FLAGS = {
        'extensions': {
            'autolink':              h.EXT_AUTOLINK,
            'disable_indented_code': h.EXT_DISABLE_INDENTED_CODE,
            'fenced_code':           h.EXT_FENCED_CODE,
            'footnotes':             h.EXT_FOOTNOTES,
            'highlight':             h.EXT_HIGHLIGHT,
            'lax_spacing':           h.EXT_LAX_SPACING,
            'no_intra_emphasis':     h.EXT_NO_INTRA_EMPHASIS,
            'quote':                 h.EXT_QUOTE,
            'space_headers':         h.EXT_SPACE_HEADERS,
            'strikethrough':         h.EXT_STRIKETHROUGH,
            'superscript':           h.EXT_SUPERSCRIPT,
            'tables':                h.EXT_TABLES,
            'underline':             h.EXT_UNDERLINE
        },

        'render_flags': {
            'escape':                h.HTML_ESCAPE,
            'expand_tabs':           h.HTML_EXPAND_TABS,
            'hard_wrap':             h.HTML_HARD_WRAP,
            'safelink':              h.HTML_SAFELINK,
            'skip_html':             h.HTML_SKIP_HTML,
            'skip_images':           h.HTML_SKIP_IMAGES,
            'skip_links':            h.HTML_SKIP_LINKS,
            'skip_style':            h.HTML_SKIP_STYLE,
            'smartypants':           h.HTML_SMARTYPANTS,
            'toc':                   h.HTML_TOC,
            'use_xhtml':             h.HTML_USE_XHTML
        }
    }

    class HoepRenderer(h.Hoep):
        def __init__(self, extensions=0, render_flags=0, tbl_class='',
                     fmt_options={}):
            super(HoepRenderer, self).__init__(extensions, render_flags)

            self._toc_ids = {}
            self._toc_patterns = (
                (r'<[^<]+?>', ''),
                (r'[^a-z0-9_.\s-]', ''),
                (r'\s+', '-'),
                (r'^[^a-z]+', ''),
                (r'^$', 'section')
            )

            self.tbl_class = tbl_class
            self.fmt_options = fmt_options

        if HAVE_PYGMENTS:
            def block_code(self, text, lang):
                """Highlight code with pygments.
                """
                return hl_with_pygments(text, lang, self.fmt_options)

        def table(self, header, body):
            content = header + body
            return tablestrap(content, self.tbl_class)

        def header(self, text, level):
            if self.render_flags & h.HTML_TOC:
                identifier = text.lower()

                for pattern, replace in self._toc_patterns:
                    identifier = re.sub(pattern, replace, identifier)

                if identifier in self._toc_ids:
                    self._toc_ids[identifier] += 1
                    identifier = '{0}-{1}'.format(identifier, self._toc_ids[identifier])
                else:
                    self._toc_ids[identifier] = 1

                return ('<h{0} id="{1}">{2}'
                        '<a class="headerlink" href="#{1}" title="Link to header title.">¶</a>'
                        '</h{0}>').format(level, identifier, text)
            else:
                return '<h{0}>{1}</h{0}>'.format(level, text)

        def preprocess(self, markdown):
            self._toc_ids.clear()
            return markdown

    def hoep_renderer(options, **kwargs):
        """
        Returns a function that can be used to transform Markdown to HTML
        using Hoep, preconfigured with the given extensions/flags.
        """
        used_exts, used_flags = xlate_exts_flags(options, HOEP_EXTS_FLAGS)
        return HoepRenderer(used_exts, used_flags, **kwargs).render

    MARKUP_RENDERERS['hoep'] = {
        'renderer': hoep_renderer,
        'options': ['extensions', 'render_flags']
    }


except ImportError:
    HAVE_HOEP = False


class MarkupProvider(object):

    def __init__(self, markup, options):
        """
        Arguments:
        - `markup`: str, 'misaka' | 'hoep'.
        - `options`: dict, has the keys: 'extensions' and 'render_flags'.
        """
        if markup not in MARKUP_RENDERERS:
            error("Unavailable markup renderer: %s", markup)
        self.markup = markup

        if ('extensions' not in options) and ('render_flags' not in options):
            error("Key error in options, must contain 'extensions' and 'render_flags'.")
        self.options = options

    def _get_option(self, option, markup_options={}):
        """
        Lookup 'option' in 'markup_options' (a dict)
        but fall back to default option if unbound.
        """
        if markup_options and (option in markup_options):
            return markup_options[option]
        else:
            return self.options[option]

    def get_renderer(self, markup_options={}, **kwargs):
        """
        Will return a function to render the item content
        based on the options specified in it. All unspecified
        options will be taken from the base configuration.
        """
        options = {}
        for option in MARKUP_RENDERERS[self.markup]['options']:
            options[option] = self._get_option(option, markup_options)

        return MARKUP_RENDERERS[self.markup]['renderer'](options, **kwargs)
