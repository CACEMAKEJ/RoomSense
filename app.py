from flask import Flask, render_template
import json

app = Flask(__name__)

alive = 0
data = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/keep_alive")
def keep_alive():
    global data, alive
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000")