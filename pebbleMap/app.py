import json
import os
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, jsonify, request, abort

from model import Plano
from view import HeatMapResponse

app = Flask(__name__)
auth_token = os.environ.get("AUTH_TOKEN", None)
if not auth_token:
    print("auth token not defined")
    exit(1)

if app.debug:
    from test_models import TestPlanoModel

    Plano.data = TestPlanoModel.mocked_data


@app.before_request
def before_request_func():
    token = request.headers.get('Authorization', request.args.get("token"))
    if not token == auth_token:
        abort(403)


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def general_params(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

        start = request.args.get('start', type=int, default=today - timedelta(days=5))
        end = request.args.get('end', type=int, default=today + timedelta(days=3))
        course_id = request.args.get('course_id', type=int, default=None)
        if not course_id:
            abort(400, "course_id is mandatory")
        return f(*args, start=start, end=end, course_id=course_id, **kwargs)

    return wrapper


def heatmap_params(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        params = dict()

        background = request.args.get('background', type=str)
        if background is not None:
            params['background'] = background

        size = request.args.get('size', type=str)
        if size is not None:
            width, height = map(int, size.split(",", 1))
            if width > 0 and height > 0:
                params['size'] = (width, height)
            else:
                abort(400, "Size (<with>,<height>) must be a positive integer!")

        return f(*args, **params, **kwargs)

    return wrapper


@app.route("/api/slots")
@general_params
def slots(start, end, course_id):
    return jsonify(Plano.slots(start, end, course_id))


@app.route("/api/occupancy")
@general_params
def occupancy(start, end, course_id):
    return jsonify(Plano.occupancy(start, end, course_id))


@app.route("/api/slots/heatmap")
@heatmap_params
@general_params
def slots_map(start, end, course_id, **kwargs):
    data = Plano.slots(start, end, course_id)
    return HeatMapResponse(data, **kwargs)


@app.route("/api/occupancy/heatmap")
@heatmap_params
@general_params
def occupancy_map(start, end, course_id, **kwargs):
    data = Plano.occupancy(start, end, course_id)
    return HeatMapResponse(data, **kwargs)
