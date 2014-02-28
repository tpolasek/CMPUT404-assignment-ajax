#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
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
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request
from flask import make_response, redirect, url_for
import json
app = Flask(__name__)
app.debug = True

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

myWorld = World()

def json_resp_entity(entity):
    if(entity is not None):
        json_entity = json.dumps(myWorld.get(entity))
    else:
        json_entity = json.dumps(myWorld.world())

    return json_entity

def flask_post_json(request):
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def root():
    return redirect(url_for('static', filename='index.html'))

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    for k,v in flask_post_json(request).iteritems():
        myWorld.update(entity,k,v)
    return json_resp_entity(entity)

@app.route("/world", methods=['POST','GET'])    
def world():
    return json_resp_entity(None)

@app.route("/entity/<entity>")    
def get_entity(entity):
    return json_resp_entity(entity)

@app.route("/clear", methods=['POST','GET'])
def clear():
    myWorld.clear()
    return "{}"

if __name__ == "__main__":
    app.run()
