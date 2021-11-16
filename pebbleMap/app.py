from datetime import datetime

from flask import Flask, jsonify

from pebbleMap.model import Plano
from view import map_response

app = Flask(__name__)

start_of_month = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
end_of_month = datetime.today().replace(day=30, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

if app.debug:
    from test_models import TestPlanoModel
    Plano.data = TestPlanoModel.mocked_data


@app.route("/api/slots")
def slots():
    return jsonify(Plano.slots(start=start_of_month, end=end_of_month, course_id=108189856))


@app.route("/api/slots/heatmap")
def slots_map():
    data = Plano.slots(start=start_of_month, end=end_of_month, course_id=108189856)
    return map_response(data)


@app.route("/api/occupancy")
def occupancy():
    return jsonify(Plano.occupancy(start=start_of_month, end=end_of_month, course_id=108189856))


@app.route("/api/occupancy/heatmap")
def occupancy_map():
    data = Plano.occupancy(start=start_of_month, end=end_of_month, course_id=108189856)
    return map_response(data)
