import random

from flask import Flask, request, session, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/')
def load_dashboard():
    return render_template("index.html")


@app.route('/set_device', methods=['POST'])
def set_device():
    data = request.json
    session["device_" + data['id']] = data['value']
    print("Updated device_" + data['id'] + ": set to " + data['value'])
    return jsonify(success=True)


@app.route('/get_temperature')
def get_temperature():
    id = request.args.get('id')
    temperature = round(random.uniform(20, 30), 1)
    return jsonify({'id': id, 'temperature': temperature})


if __name__ == '__main__':
    app.run()
