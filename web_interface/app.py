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
    with Session(engine) as session:
        matches_list = db_manager.get_matches(session=session)
        return render_template("matches.html", matches=matches_list)


@app.route("/add_match", methods=["POST", "GET"])
def add_match():
    with Session(engine) as session:
        if request.method == "POST":
            team_name_1 = request.form["team_1"]
            team_name_2 = request.form["team_2"]
            points_team_1 = request.form["points_team_1"]
            points_team_2 = request.form["points_team_2"]
            try:
                points_team_1 = int(points_team_1)
                points_team_2 = int(points_team_2)
            except:
                return "Ошибка входных данных"

            res = db_manager.create_match(session=session, points_team_1=points_team_1, points_team_2=points_team_2,
                                          team_name_1=team_name_1, team_name_2=team_name_2)
            if res:
                return render_template("add_player.html")
            else:
                return "Ошибка входных данных"
        else:
            return render_template("add_match.html")


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


@app.route("/add_team", methods=["POST", "GET"])
def add_team():
    with Session(engine) as session:
        if request.method == "POST":
            team_name = request.form["team_name"]
            res = db_manager.create_team(team_name=team_name, session=session)
            if res:
                return render_template("add_team.html")
            else:
                return "При добавлении произошла ошибка"
        else:
            return render_template("add_team.html")



@app.route("/team/<int:id>")
def team(id):
    return "team" + str(id)


# db_manager.create_bd()
# with Session(engine) as session:
#     db_manager.create_player(player_name="Hearlod", team_name=None, session=session)
#     db_manager.create_player(player_name="Bob", team_name=None, session=session)
#     db_manager.create_player(player_name="Steave", team_name=None, session=session)
#     db_manager.create_player(player_name="John", team_name=None, session=session)
#     db_manager.create_player(player_name="Pop", team_name=None, session=session)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)
