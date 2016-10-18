# -*- coding: utf-8 -*-

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import json
import requests

import flex
from flex.exceptions import ValidationError

from lib.config import Config

config = Config('config.cfg', True)

class SwaggerProxy(resource.Resource):

    isLeaf = True

    def _get_host(self):
        return config.options['api']['url']

    def render_GET(self, request):
        api_response = requests.get(self._get_host() + request.path, headers=request.getAllHeaders())
        return self._process_swagger(request, api_response)

    def render_POST(self, request):
        api_response = requests.post(self._get_host() + request.path, data = request.content.read(), headers=request.getAllHeaders())
        return self._process_swagger(request, api_response)

    def render_DELETE(self, request):
        api_response = requests.delete(self._get_host() + request.path, data = request.content.read(), headers=request.getAllHeaders())
        return self._process_swagger(request, api_response)

    def _process_swagger(self, request, api_response):
        api_response.headers['Content-Type'] = 'application/json'
        schema = flex.load(config.options['swagger']['file'])

        response_content = api_response.content
        api_validity = True
        try:
            flex.core.validate_api_call(schema, raw_request=api_response.request, raw_response=api_response)
        except ValidationError as err:
            api_validity = False
            json_data = json.loads(api_response.content)
            json_data['_swagger_validation'] = err.detail
            response_content = json.dumps(json_data)

        for row in api_response.headers:
            if row in ('Content-Encoding', 'Content-Length', 'Date', 'Connection'):
                continue
            request.setHeader(row, api_response.headers[row])
            request.setHeader('SWAGGER-PROXY-VALID', 'Valid' if api_validity else 'Invalid')
        return response_content

def run():
    endpoints.serverFromString(reactor, "tcp:%s" % (config.options['proxy']['port'])).listen(server.Site(SwaggerProxy()))
    reactor.run()

if __name__ == '__main__':
    run()
