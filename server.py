#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import web
import preview


markdown_demo = web.template.frender('demo.html')


class MarkdownPreview():
    """
    [Ajax]: Markdown content preview.
    """
    def GET(self):
        return markdown_demo()

    def POST(self):
        markdown_content = web.input()
        post_preview = preview.markdown(markdown_content['data'])
        return post_preview

app = web.application()
app.add_mapping('/', MarkdownPreview)


if __name__ == '__main__':
    app.run()
