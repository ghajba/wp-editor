__author__ = 'GHajba'

from html2text import HTML2Text
import re
import json

class Xml2Md(HTML2Text):
    def __init__(self, out=None, baseurl=''):
        HTML2Text.__init__(self, baseurl=baseurl)
    def feed(self, data):
        data = data.replace("[/sourcecode]", "</sourcecode>")
        data = data.replace("[sourcecode", "<sourcecode")
        for i in [m.start() for m in re.finditer('<sourcecode', data)]:
            j = data.find("]", i)
            data = data[:j] + ">" +data[j+1:]

        HTML2Text.feed(self, data)

    def handle_tag(self, tag, attrs, start):
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)
        if tag in ['sourcecode']:
            if start:
                self.o("~~~~~~~~"+json.dumps(attrs, indent=0)+"\n")
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

def xml2md(xml, baseurl=''):
    h = Xml2Md(baseurl=baseurl)
    return h.handle(xml)
