import random
import json
import os
from flask import Flask, request, session, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

filename = "config.json"


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
    id = request.args.get('id')
    temperature = round(random.uniform(12, 31), 1)
    return jsonify({'id': id, 'temperature': temperature})


def write_thresholds_to_file(upper_threshold, lower_threshold):
    data = {
        "upperThreshold": upper_threshold,
        "lowerThreshold": lower_threshold
    }
    with open(filename, "w") as file:
        json.dump(data, file)


def load_file():
    if not os.path.exists(filename):
        upper_threshold = 20
        lower_threshold = 0
        write_thresholds_to_file(upper_threshold, lower_threshold)
    else:
        with open(filename, "r") as file:
            data = json.load(file)
            upper_threshold = data.get("upperThreshold")
            lower_threshold = data.get("lowerThreshold")
    session["upperThreshold"] = upper_threshold
    session["lowerThreshold"] = lower_threshold
    return data


if __name__ == '__main__':
    app.run()
