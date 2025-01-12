from flask import Flask, render_template, jsonify, request
import json
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

uri = os.getenv('MONGODB_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.roomtemp

temperatureCollection = db["temperatures"]
humidityCollection = db["humidities"]


alive = 0
data = {}

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/sensors")
def sensors():
    return render_template("sensors.html")

@app.route("/history")
def history():
    temperatures = []
    humidities = []

    for reading in temperatureCollection.find().sort("Time", -1):
        reading["Temperature"] = str(reading['Temperature'])
        reading["Time"] = reading['Time'].strftime("%b %d %Y %H:%M")
        temperatures.append(reading)
    for reading in humidityCollection.find().sort("Time", -1):
        reading["Humidity"] = str(reading['Humidity'])
        reading["Time"] = reading['Time'].strftime("%b %d %Y %H:%M")
        humidities.append(reading)

    return render_template("history.html", temperatures = temperatures, humidities = humidities)


@app.route("/keep_alive")
def keep_alive():
    global data, alive
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)