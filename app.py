from flask import Flask, request, session, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/')
def load_dashboard():
    return render_template("index.html")


@app.route('/set_device', methods=['POST'])
def set_device():
    data = request.json
    session["device_"+data['id']] = data['value']
    print("Updated device_" + data['id'] + ": set to " + data['value'])
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
