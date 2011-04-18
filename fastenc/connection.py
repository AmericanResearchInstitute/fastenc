"""
Objects related to connecting to and retrieving results from encoding.com

"""

from xml.etree.ElementTree import fromstring, tostring

import httplib
import logging
import urlparse
import urllib

logger = logging.getLogger('fastenc.connection')

class ConnectionFailed(Exception):
    def __init__(self, status=None, reason=None):
        Exception.__init__(self)
        self.status = status
        self.reason = reason

class Connection(object):
    def __init__(self, secure):
        # Encoding.com has just the one API server, but HTTPS is optional
        if (secure):
            self.url = urlparse.urlsplit('https://manage.encoding.com:443')
            self.webservice = httplib.HTTPSConnection(self.url.netloc)
        else:
            self.url = urlparse.urlsplit('http://manage.encoding.com:80')
            self.webservice = httplib.HTTPConnection(self.url.netloc)

    def request(self, query):
        '''
>>> params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
>>> headers = {"Content-type": "application/x-www-form-urlencoded",
...            "Accept": "text/plain"}
>>> conn = httplib.HTTPConnection("musi-cal.mojam.com:80")
>>> conn.request("POST", "/cgi-bin/query", params, headers)
>>> response = conn.getresponse()
        '''
        query_string = tostring(query, encoding='UTF-8')

        params = urllib.urlencode({'xml': query_string})

        headers = {'User-Agent': 'Encoding.com Python API',
                   'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        logger.debug('Sending query string:')
        logger.debug(query_string)

        # get the response
        self.webservice.request('POST', '/', params, headers)
        response = self.webservice.getresponse()

        logger.debug('Response: %s %s', response.status, response.reason)

        if response.status == 200:
            data = response.read()

            logger.debug('Returned data:')
            logger.debug(data)

            return fromstring(data)
        else:
            raise ConnectionFailed(response.status, response.reason)

