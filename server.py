#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import web
import mdparser


markdown_demo = web.template.frender('demo.html')


MISAKA_DEFAULTS = {
    'extensions': [
        'fenced_code',
        'highlight',
        'no_intra_emphasis',
        'tables',
        'autolink',
        'space_headers',
        'strikethrough',
        'superscript'
    ],
    'render_flags': ['skip_html']
}

HOEP_DEFAULTS = {
    'extensions': [
        'autolink',
        'fenced_code',
        'footnotes',
        'no_intra_emphasis',
        'strikethrough',
        'tables',
        'space_headers',
        'superscript'
    ],
    'render_flags': ['safelink', 'skip_html', 'smartypants']
}

TABLE_CLASS = 'table table-striped table-bordered table-hover'

m_renderer = (mdparser.MarkupProvider('misaka', MISAKA_DEFAULTS)
              .get_renderer(tbl_class=TABLE_CLASS, fmt_options={
                  'linenos': 'table'
              }))
h_renderer = (mdparser.MarkupProvider('hoep', HOEP_DEFAULTS)
              .get_renderer(tbl_class=TABLE_CLASS, fmt_options={
                  'linenos': 'table'
              }))


class MarkdownPreview():
    """
    [Ajax]: Markdown content preview.
    """
    def GET(self):
        return markdown_demo()

    def POST(self):
        markdown_content = web.input()

        # use the Misaka markdown parser
        post_preview = m_renderer(markdown_content['data'])

        # use the Hoep markdown parser
        # post_preview = h_renderer(markdown_content['data'])

        return post_preview


app = web.application()
app.add_mapping('/', MarkdownPreview)


if __name__ == '__main__':
    app.run()
