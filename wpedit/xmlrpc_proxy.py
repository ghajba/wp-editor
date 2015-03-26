__author__ = 'GHajba'
"""
Provides HTTP and HTTPS proxy support for Python's xmlrpclib, via urllib2.

Usage:
    transport = HTTPProxyTransport({'http': <proxy host and port as string>,'https': <proxy host and port as string>,})
"""

import urllib2
import xmlrpclib


class Urllib2Transport(xmlrpclib.Transport):
    def __init__(self, opener=None, https=False, use_datetime=0, verbose=False):
        xmlrpclib.Transport.__init__(self, use_datetime)
        self.opener = opener or urllib2.build_opener()
        self.https = https
        self.verbose = verbose

    def request(self, host, handler, request_body, verbose=0):
        protocol = ('http', 'https')[bool(self.https)]
        req = urllib2.Request('%s://%s%s' % (protocol, host, handler), request_body)
        req.add_header('User-agent', self.user_agent)
        self.verbose = verbose
        return self.parse_response(self.opener.open(req))


class HTTPProxyTransport(Urllib2Transport):
    def __init__(self, proxies, use_datetime=0):
        opener = urllib2.build_opener(urllib2.ProxyHandler(proxies))
        Urllib2Transport.__init__(self, opener, https=True, use_datetime=use_datetime)