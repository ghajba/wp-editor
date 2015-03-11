__author__ = 'GHajba'

from html2text import HTML2Text
import re
import json


class Xml2Md(HTML2Text):
    def __init__(self, out=None, baseurl=''):
        HTML2Text.__init__(self, baseurl=baseurl)
        # because we do not need line wrapping in paragraphs
        self.body_width = 0

    def feed(self, data):
        data = data.replace("[/sourcecode]", "</sourcecode>")
        data = data.replace("[sourcecode", "<sourcecode")
        for i in [m.start() for m in re.finditer('<sourcecode', data)]:
            j = data.find("]", i)
            data = data[:j] + ">" + data[j + 1:]

        HTML2Text.feed(self, data)

    def handle_tag(self, tag, attrs, start):
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)
        if tag in ['sourcecode']:
            if start:
                self.o("~~~~~~~~" + json.dumps(attrs, indent=0) + "\n")
                self.startpre = 1
                self.pre = 1
            else:
                self.pre = 0
                self.o("\n")
                self.o("~~~~~~~~\n")
        elif tag == "pre":
            self.o("@@@")
        else:
            HTML2Text.handle_tag(self, tag, attrs, start)

    def handle_comment(self, comment_content):
        """ override comment handling """
        if "more" == comment_content:
            self.o("\n--------\n")
        else:
            self.o("# " + comment_content)


def xml2md(xml, baseurl=''):
    h = Xml2Md(baseurl=baseurl)
    return h.handle(xml)

if __name__ == "__main__":
    xml = """<p>This is a test post with my md2xml plugin</p>
<p>I am writing a simple Python application, which can convert text written in a specific dialect of mark-down text to a WordPress post.</p>
<p>I do this to have one open-source offline application which helps me to write articles on my commuting to work -- in a way I know from LeanPub.</p>
<p>And this is the first part of the application...</p>
<!--more-->

"""
    print xml2md(xml)
