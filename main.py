import requests
from flask import Flask, render_template, request
from pprint import pprint
import os

from config import api_key

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/weather', methods=['GET'])
def weather():
    q = request.args.get("city_name")
    unit = "metric"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={unit}"
    data = requests.get(url=url)
    return render_template("weather.html", data=data.json())


if __name__ == '__main__':
    app.run(debug=True)
