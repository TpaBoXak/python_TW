from flask import Flask
from flask import request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import FLASK_DEBUG, SQLALCHEMY_URL, SQLALCHEMY_ECHO

from work_with_data import db_manager


engine = create_engine(
    url=SQLALCHEMY_URL,
    echo=SQLALCHEMY_ECHO,
)

app = Flask(__name__)


@app.route("/")
@app.route("/matches")
def matches():
    return render_template("matches.html")


@app.route("/add_match")
def add_match():
    return render_template("teams.html")


@app.route("/match/<int:id>")
def match(id):
    return "Matches" + str(id)


@app.route("/investors")
def investors():
    return render_template("investors.html")


@app.route("/investor/<int:id>")
def investor(id):
    return "investor" + str(id)


@app.route("/players")
def players():
    with Session(engine) as session:
        players_list = db_manager.get_players(session=session)
        return render_template("players.html", players=players_list)


@app.route("/add_player", methods=["POST", "GET"])
def add_player():
    with Session(engine) as session:
        if request.method == "POST":
            player_name = request.form["player_name"]
            team_name = request.form["team_name"]
            res = db_manager.create_player(player_name=player_name, team_name=team_name, session=session)
            if res:
                return render_template("add_player.html")
            else:
                return "При добавлении произошла ошибка"
        else:
            return render_template("add_player.html")


@app.route("/player/<int:id>")
def player(id):
    return "player" + str(id)


@app.route("/teams")
def teams():
    with Session(engine) as session:
        teams_list = db_manager.get_teams(session=session)
        return render_template("teams.html", teams=teams_list)






@app.route("/team/<int:id>")
def team(id):
    return "team" + str(id)


# db_manager.create_bd()
# db_manager.create_player("Hearlod", None)
# db_manager.create_player("Bob", None)
# db_manager.create_player("Steave", None)
# db_manager.create_player("John", None)
# db_manager.create_player("Pop", None)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)
