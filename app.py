import random
import time
import threading

from flask import Flask, request, session, jsonify, render_template
from temperatureUtils import increase_temperature, decrease_temperature
from fileUtils import write_thresholds_to_file, load_file
from windowTkinter import start_tinker

app = Flask(__name__)
app.secret_key = 'seowsk1gc'

@app.route('/')
def load_dashboard():
    load_file()
    return render_template("index.html")


@app.route('/set_device', methods=['POST'])
def set_device():
    data = request.json
    session["device_" + data['id']] = data['value']
    print("Updated device_" + data['id'] + ": set to " + data['value'])
    return jsonify(success=True)


@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    data = request.json
    session["upperThreshold"] = data['value']['upperThreshold']
    session["lowerThreshold"] = data['value']['lowerThreshold']
    print("Updated thresholds: set to " + data['value']['lowerThreshold'] +
          " - " + data['value']['upperThreshold'])
    write_thresholds_to_file(session["upperThreshold"], session["lowerThreshold"])
    return jsonify(success=True)


@app.route('/get_temperature')
def get_temperature():
    thermostat_id = request.args.get("id")
    heater = request.args.get('heater')

    history_key = "thermostatHistory_" + thermostat_id
    heater_key = "heaterStatus_"+heater

    if "lowerThreshold" not in session or "upperThreshold" not in session:
        load_file()

    lower_threshold = float(session["lowerThreshold"])
    upper_threshold = float(session["upperThreshold"])

    if heater_key not in session:
        session[heater_key] = False
    if history_key not in session:
        session[history_key] = []

    new_temperature = None

    if len(session[history_key]) == 0:
        new_temperature = round(random.uniform(12, 31), 1)
        print(new_temperature)
    else:
        prev_temperature = float(session[history_key][-1]["temperature"])
        if prev_temperature < lower_threshold:
            print("CASE 1")
            session[heater_key] = True
            print("Heater is ON")
            print(session[heater_key])
            new_temperature = increase_temperature(prev_temperature)
            print(new_temperature)
        elif prev_temperature > upper_threshold:
            print("CASE 2")
            session[heater_key] = False
            print("Heater is OFF")
            print(session[heater_key])
            new_temperature = decrease_temperature(prev_temperature)
            print(new_temperature)
        elif session[heater_key]:
            print("CASE 3")
            new_temperature = increase_temperature(prev_temperature)
            print(new_temperature)
        elif not session[heater_key]:
            print("CASE 4")
            new_temperature = decrease_temperature(prev_temperature)
            print(new_temperature)

        if new_temperature < lower_threshold:
            session[heater_key] = True
        elif new_temperature > upper_threshold:
            session[heater_key] = False

    updated_history = session[history_key] + [{
        "timestamp": time.time(),
        "temperature": new_temperature
    }]
    session.pop(history_key, default=None)
    session[history_key] = updated_history

    print(session[history_key])
    return jsonify({'id': thermostat_id, 'temperature': new_temperature})


@app.route("/get_random_temperature")
def get_random_temperature():
    return jsonify({'id': request.args.get("id"), 'temperature': round(random.uniform(12, 31), 1)})


@app.route("/get_temperature_history")
def get_temperature_history():
    thermostat_id = request.args.get("id")
    history_key = "thermostatHistory_" + thermostat_id
    if history_key not in session:
        session[history_key] = []
    return jsonify({'id': thermostat_id, 'history': session[history_key]})


@app.route("/get_heater_status")
def get_heater_status():
    id = request.args.get("id")
    if "heaterStatus_"+id not in session:
        session["heaterStatus_"+id] = False
    return jsonify({'id': id, 'status': session["heaterStatus_"+id]})


def start_flask():
    app.run()


if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    start_tinker()
