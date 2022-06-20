import requests
from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy
from config import api_key
from sqlalchemy_pagination import paginate

app = Flask(__name__)

db = SQLAlchemy("sqlite:///db.sqlite")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def index():
    page = request.args.get("page")

    if not page:
        page = 1

    messages_query = db.query(Message)

    messages = paginate(query=messages_query, page=int(page), page_size=5)

    return render_template("index.html", messages=messages)


@app.route('/add_message', methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    message = Message(author=username, text=text)
    message.save()

    return redirect("/")


@app.route('/weather', methods=['GET'])
def weather():
    q = request.args.get("city_name")
    unit = "metric"

    url = f"https://api.openweathermap.org/data/2.5/weather"
    print(api_key)
    data = requests.get(url=url, params={'q': q, 'units': unit, 'api_key': api_key, })
    print(data.json())
    return render_template("weather.html", data=data.json())


if __name__ == '__main__':
    app.run(debug=True)
