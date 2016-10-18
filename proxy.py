# -*- coding: utf-8 -*-

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import json
import requests

import flex
from flex.exceptions import ValidationError

class Counter(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        api_response = requests.get("http://localhost:8090" + request.path, headers=request.getAllHeaders())
        return self._process_swagger(request, api_response)

    def render_POST(self, request):
        api_response = requests.post("http://localhost:8090" + request.path, data = request.content.read(), headers=request.getAllHeaders())
        return self._process_swagger(request, api_response)

    def render_DELETE(self, request):
        api_response = requests.delete("http://localhost:8090" + request.path, data = request.content.read(), headers=request.getAllHeaders())
        return self._process_swagger(request, api_response)

    def _process_swagger(self, request, api_response):
        api_response.headers['Content-Type'] = 'application/json'
        schema = flex.load('core.yaml')

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
    endpoints.serverFromString(reactor, "tcp:8000").listen(server.Site(Counter()))
    reactor.run()

if __name__ == '__main__':
    run()
