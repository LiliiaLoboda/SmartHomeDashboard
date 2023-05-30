import json
import os
from flask import session

filename = "config.json"


def write_thresholds_to_file(upper_threshold, lower_threshold):
    data = {
        "upperThreshold": upper_threshold,
        "lowerThreshold": lower_threshold
    }
    with open(filename, "w") as file:
        json.dump(data, file)


def load_file():
    if not os.path.exists(filename):
        upper_threshold = 23.7
        lower_threshold = 22.9
        data = {'upperThreshold': upper_threshold, 'lowerThreshold': lower_threshold}
        write_thresholds_to_file(upper_threshold, lower_threshold)
    else:
        with open(filename, "r") as file:
            data = json.load(file)
            upper_threshold = data.get("upperThreshold")
            lower_threshold = data.get("lowerThreshold")
    session["upperThreshold"] = upper_threshold
    session["lowerThreshold"] = lower_threshold
    return data


def load_file_without_session():
    if not os.path.exists(filename):
        upper_threshold = 23.7
        lower_threshold = 22.9
        data = {'upperThreshold': upper_threshold, 'lowerThreshold': lower_threshold}
        write_thresholds_to_file(upper_threshold, lower_threshold)
    else:
        with open(filename, "r") as file:
            data = json.load(file)
            upper_threshold = data.get("upperThreshold")
            lower_threshold = data.get("lowerThreshold")
    return data