## README

[Pagedown](https://code.google.com/p/pagedown/) is really simple to use. However, the **Markdown-to-HTML** converter it provided
is simple too(too simple) that we may want a more powerful one. And I think the best method is to use the converter on the **server** side, because there are many Markdown parsers you can choose from and most of them are powerful enough.

I delete the code of Pagedown's JavaScript Markdown converter and live previewer. To preview the markdown content user-inputted, in this demo, the markdown content will be sent to the server with AJAX and converted at the server side, then get back the HTML and render the HTML content into the page. *Bootstrap* is used to control the page style.

To resize the textarea of the editor(just like what StackOverFlow does), I use a script from [here](https://github.com/vasanth-v/Jquery-textarea-resize-autogrow).


## Requirements

+ [web.py](http://www.webpy.org)
+ [pygments](http://pygments.org)
+ [misaka](http://misaka.61924.nl/)
+ [hoep](https://github.com/Anomareh/Hoep)


## Installation

You could use `pip` to install all the required python packages:

```pip install -U web.py pygments misaka hoep```

And then execute the command `python server.py` or `./server.py` in terminal and visit the address `http://0.0.0.0:8080/`. (**Note**: Only tested in *Chrome* and *Safari*.)


## Screenshots

The editor:

![Pagedown-Editor](https://raw.github.com/galeo/pagedown-editor-only/master/static/images/pagedown.png)

Content preview:

![Content-Preview](https://raw.github.com/galeo/pagedown-editor-only/master/static/images/preview.png)
