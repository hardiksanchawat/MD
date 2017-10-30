# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from boto3 import dynamodb
import boto3.dynamodb.table
from boto3.dynamodb.conditions import Key, Attr
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = makeYqlQuery(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
def makeYqlQuery(req):
    if req.get("result").get("action") != "AHepatitisHepatitisA":
        return {}
    result = req.get("result")
    query = result.get("resolvedQuery")
	
    ddb = boto3.client('dynamodb', aws_access_key_id='', aws_secret_access_key='', region_name='')
	
    response = ddb.list_tables()
	
    # For a Boto3 service resource
    dynamodb = boto3.resource('dynamodb', aws_access_key_id='', aws_secret_access_key='', region_name='')
    table = dynamodb.Table('medical_qa_details')
    response = table.scan(FilterExpression=Attr('questions').eq(query))
    speech=response['Items'][0]['answers']
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "medical"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')