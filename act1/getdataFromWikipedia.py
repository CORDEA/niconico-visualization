#!/bin/env python
# encoding:utf-8
#

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2014-11-21"

import sys, urllib2
from HTMLParser import HTMLParser

class ChParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.br = 0
        self.sentense = ""
        self.flag = False
        self.sflag = False
        self.count = 0
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'tr' == tag:
            self.flag = True
        if 'td' == tag and self.flag:
            self.count += 1
        if self.count == 2 and 'a' == tag and 'title' in attrs:
            self.sflag = True

    def handle_endtag(self, tag):
        if 'tr' == tag:
            self.count = 0
            self.flag = False

    def handle_data(self, data):
        if self.sflag:
            print data.encode('utf-8')
            self.sflag = False

if __name__ == '__main__':
    url = sys.argv[1]
    response = urllib2.urlopen(url)
    html = response.read()

    parser = ChParser()
    parser.feed(html.decode('utf-8'))
    parser.close()
