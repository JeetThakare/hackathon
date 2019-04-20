# Copyright 2016 Google Inc.
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

import logging

from flask import Flask, jsonify, request
import flask_cors

from models.event import Event
from models.enrollment import Enrollment

import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)


@app.route('/events', methods=['GET'])
def list_events():
    """Returns a list of events"""

    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    events = Event.get_all_events()

    return jsonify(events)


@app.route('/events', methods=['POST', 'PUT'])
def add_event():
    """
    Add event with format as:

        {
            'description': "placeholder",
            'startdt': "placeholder",
            'enddt': "placeholder",
            'location': "placeholder",
            'teacher_name': "placeholder",
            'teacher_email': "placeholder",
        }
    """

    # Verify Firebase auth.
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    data = request.get_json()

    if Event.add_event(data, claims['name'], claims['email']):
        return 'OK', 200
    return 'Error inserting Event', 500


@app.route('/enroll', methods=['POST', 'PUT'])
def enroll():
    # Verify Firebase auth.
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    data = request.get_json()

    try:
        Enrollment.enroll(claims['email'], data['key'])
        return 'OK', 200
    except Exception as e:
        logging.error("error enrolling ", str(e))
    return "Error", 500


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
