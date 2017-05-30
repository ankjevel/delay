# -*- coding: utf-8 -*-

"""
delay.core
"""

import os
import time
import argparse

from flask import Flask, Response, g, request, jsonify as flask_jsonify
from flask_common import Common
from werkzeug.wrappers import BaseResponse


BaseResponse.autocorrect_location_header = False

app = Flask(__name__)
app.debug = bool(os.environ.get('DEBUG'))

common = Common(app)


def jsonify(*args, **kwargs):
    response = flask_jsonify(*args, **kwargs)
    if not response.data.endswith(b'\n'):
        response.data += b'\n'
    return response


@app.before_request
def before_request():
    """Set timers for request-time"""
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.after_request
def set_cors_headers(response):
    """Allow the world."""

    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Max-Age'] = '3600'
        if request.headers.get('Access-Control-Request-Headers') is not None:
            response.headers['Access-Control-Allow-Headers'] = request.headers['Access-Control-Request-Headers']
    return response


@app.route('/<delay>')
def delay_response(delay):
    """Delayed resonse, at the most one hour"""

    delay = min(float(delay), 60 * 60)

    time.sleep(delay)

    return jsonify(dict(
        origin=request.headers.get('X-Forwarded-For', request.remote_addr),
        headers=dict(request.headers.items()),
        request_time=g.request_time(),
    ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    app.run(port=args.port, host=args.host)
