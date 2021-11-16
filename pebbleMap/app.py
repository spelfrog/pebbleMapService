from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, jsonify, request, abort

from pebbleMap.model import Plano
from view import HeatMapResponse

app = Flask(__name__)

if app.debug:
    from test_models import TestPlanoModel

    Plano.data = TestPlanoModel.mocked_data


def general_params(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

        start = request.args.get('start', type=int, default=today - timedelta(days=5))
        end = request.args.get('end', type=int, default=today + timedelta(days=3))
        course_id = request.args.get('course_id', type=int, default=None)
        print("general_params")
        if not course_id:
            abort(400, "course_id is mandatory")
            print("after raise")
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
