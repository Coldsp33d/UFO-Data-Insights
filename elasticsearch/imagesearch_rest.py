#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from girder import events
from girder.api import access
from girder.api.describe import Description
from girder.api.rest import Resource
from .settings import ImageSpaceSetting

import json
import requests

setting = ImageSpaceSetting()

#ENV IMAGE_SPACE_ELASTIC_SEARCH=http://localhost:9200/imagespace
class ImageSearch(Resource):
    def __init__(self):
        self.resourceName = 'imagesearch'
        self.route('GET', (), self.getImageSearch)

    @access.public
    def getImageSearch(self, params):
        return self._imageSearch(params)

    @access.public
    def postImageSearch(self, params):
        return self._imageSearch(params)

    def _imageSearch(self, params):
        limit = params['limit'] if 'limit' in params else '100'
        query = params['query'] if 'query' in params else { "match_all":{} }
        offset = params['offset'] if 'offset' in params else '0'
        base = 'http://imagespace-elasticsearch:9200/imagespace' + '/_search'

        qparams = { "query":{ "match_all":{} }, "size":limit, "from":offset }

        # Give plugins a chance to adjust the Solr query parameters
        event = events.trigger('imagespace.imagesearch.qparams', qparams)
        for response in event.responses:
            qparams = response

        try:
            result = requests.get(base, data=json.dumps(qparams), headers={'Content-Type':'application/json'}).json()
        except ValueError:
            return []

        docs = []
        try:
            for row in result['hits']['hits']:
                doc = {}
                doc['id'] = row['_source']['id']
                doc['sha1sum_s_md'] = row['_source']['sha1sum_s_md']
                docs.append(doc)
        except KeyError:
            return {
                'numFound': 0,
                'docs': docs
            }

        response = {
            'numFound': result['_shards']['total'],
            'docs': docs
        }

        # Give plugins a chance to adjust the end response of the imagesearch
        event = events.trigger('imagespace.imagesearch.results', response)
        for eventResponse in event.responses:
            response = eventResponse

        return response
    getImageSearch.description = Description('Searches image database')
    # @todo document params
