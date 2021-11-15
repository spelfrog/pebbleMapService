from datetime import datetime

from flask import Flask, jsonify

from pebbleMap.model import Plano

app = Flask(__name__)

start_of_month = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
end_of_month = datetime.today().replace(day=30, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)


@app.route("/api/slots")
def slots():
    return jsonify(Plano.slots(start=start_of_month, end=end_of_month, course_id=108189856))


@app.route("/api/occupancy")
def heatmap():
    return jsonify(Plano.occupancy(start=start_of_month, end=end_of_month, course_id=108189856))
