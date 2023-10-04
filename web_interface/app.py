from flask import Flask
from flask import render_template
from config import FLASK_DEBUG

app = Flask(__name__)


@app.route("/")
@app.route("/matches")
def matches():
    return "Matches"


@app.route("/match/<int:id>")
def match(id):
    return "Matches" + str(id)


@app.route("/investors")
def investors():
    return "investors"


@app.route("/investor/<int:id>")
def investor(id):
    return "investor" + str(id)


@app.route("/players")
def players():
    return "players"


@app.route("/player/<int:id>")
def player(id):
    return "player" + str(id)

@app.route("/teams")
def teams():
    return "teams"


@app.route("/team/<int:id>")
def team(id):
    return "team" + str(id)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)
