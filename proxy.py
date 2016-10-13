# Originally from http://sharebear.co.uk/blog/2009/09/17/very-simple-python-caching-proxy/
#
# Usage:
# A call to http://localhost:80000/example.com/foo.html will cache the file
# at http://example.com/foo.html on disc and not redownload it again. 
# To clear the cache simply do a `rm *.cached`. To stop the server simply
# send SIGINT (Ctrl-C). It does not handle any headers or post data. 

import BaseHTTPServer
import hashlib
import os
import urllib2
from StringIO import StringIO
import gzip

from flex.exceptions import ValidationError
from swagger_parser import SwaggerParser
import flex
import requests

class CacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        return self.do_GET_requests()

    def do_GET_requests(self):
        schema = flex.load('core.yaml')
        response = requests.get("http://localhost:8090" + self.path, headers=self.headers)
        response.headers['Content-Type'] = 'application/json'
        #api_validity = True
        #try:
        #    res = flex.core.validate_api_call(schema, raw_request=response.request, raw_response=response)
        #except ValidationError as err:
        #    error = err
        #    api_validity = False

        self.send_response(200)
        i = 0
        for row in response.headers:
            if row in ('Content-Encoding', 'Content-Type', 'Content-Length'):
                continue
            self.send_header(row, response.headers[row])
        #self.send_header('Content-Type', 'application/json')
        self.send_header('SWAGGER-PROXY-VALID', 'Valid' if api_validity else 'Invalid')
        self.end_headers()
        #self.send_response(200, data)
        self.wfile.writelines(response.content)

    def do_GET_urllib(self):
        #print "Opening http://localhost:8090" + self.path
        request = urllib2.Request("http://localhost:8090" + self.path, headers=self.headers)
        response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()

        schema = flex.load('core.yaml')
        res = flex.core.validate_api_call(schema, raw_request=request, raw_response=response)
        print res

        self.send_response(200)
        for row in response.info().headers:
            header_row = row.split(':')
            print "%s: %s" % (header_row[0].strip(' \t\n\r'), header_row[1].strip(' \t\n\r'))
            if header_row[0].strip(' \t\n\r') in ('Content-Encoding'):
                continue
            self.send_header(header_row[0].strip(' \t\n\r'), header_row[1].strip(' \t\n\r'))
        self.end_headers()
        #self.send_response(200, data)
        self.wfile.writelines(data)

def run():
    server_address = ('', 8000)
    httpd = BaseHTTPServer.HTTPServer(server_address, CacheHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
