from flask import redirect, url_for
from flask import request
from flask import render_template

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Blueprint

from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from . import db_manager
engine = create_engine(
    url=SQLALCHEMY_URL,
    echo=SQLALCHEMY_ECHO,
)

bp = Blueprint('routes', __name__)

@bp.route("/")
@bp.route("/matches")
def matches():
    with Session(engine) as session:
        matches_list = db_manager.get_matches(session=session)
        teams_list = db_manager.get_teams(session=session)
        return render_template("matches.html", matches=matches_list, teams=teams_list)


@bp.route("/add_match", methods=["POST", "GET"])
def add_match():
    with Session(engine) as session:
        if request.method == "POST":
            match_name = request.form["match_name"]
            if match_name == "":
                return "Введите навзвание матча"
            team_name_1 = request.form["team_1"]
            team_name_2 = request.form["team_2"]

            if team_name_1 == team_name_2:
                return "Выбрана одна и та же команда"
            points_team_1 = request.form["points_team_1"]
            points_team_2 = request.form["points_team_2"]
            try:
                points_team_1 = int(points_team_1)
                points_team_2 = int(points_team_2)
            except:
                return "Ошибка входных данных"

            res = db_manager.create_match(session=session, points_team_1=points_team_1, points_team_2=points_team_2,
                                          team_name_1=team_name_1, team_name_2=team_name_2, match_name=match_name)
            if res:
                return redirect(url_for("routes.add_match"))
            else:
                return "Ошибка добавление записи в базу данных"
        else:
            teams_list = db_manager.get_teams(session=session)
            return render_template("add_match.html", teams=teams_list)


@bp.route("/remove_match/<string:match_name>", methods=["GET", "POST"])
def remove_match(match_name):
    if request.method == "GET":
        with Session(engine) as session:
            res = db_manager.remove_match(session=session, match_name=match_name)
            if res:
                return redirect(url_for("routes.matches"))
            else:
                return "Ошибка удаления"
    else:
        return redirect(url_for("routes.matches"))


@bp.route("/update_match/<string:match_name_old>", methods=["GET", "POST"] )
def update_match(match_name_old):
    if request.method == "POST":
        match_name_new = request.form["match_name_new"]
        team_1_name_new = request.form["team_1_name_new"]
        team_2_name_new = request.form["team_2_name_new"]
        points_1_new = request.form["points_1_new"]
        points_1_new = int(points_1_new)
        points_2_new = request.form["points_2_new"]
        points_2_new = int(points_2_new)

        if team_1_name_new == team_2_name_new:
            return "Выбрана одна и та же команда"
        if match_name_new == "" or match_name_old == "" or points_2_new is None or points_1_new is None:
            return "Ошибка входных значений"
        if team_1_name_new == "" or team_2_name_new == "":
            return "Ошибка входных значений"

        with Session(engine) as session:
            res = db_manager.update_match(
                session=session, match_name_old=match_name_old, match_name_new=match_name_new,
                points_2_new=points_2_new, team_1_name_new=team_1_name_new,
                team_2_name_new=team_2_name_new, points_1_new=points_1_new
            )
            if res:
                return redirect(url_for("routes.matches"))
            else:
                return "Ошибка в изменении матча"
    else:
        return redirect(url_for("routes.matches"))


@bp.route("/investors")
def investors():
    with Session(engine) as session:
        investors_list = db_manager.get_investors(session=session)
        teams_list = db_manager.get_teams(session=session)
        return render_template("investors.html", investors=investors_list, teams=teams_list)


@bp.route("/add_investor", methods=["POST", "GET"])
def add_investor():
    with Session(engine) as session:
        if request.method == "POST":
            investor_name = request.form["investor_name"]
            if investor_name == "":
                return "введите имя инвестора"
            res = db_manager.create_investor(investor_name=investor_name, session=session)
            if res:
                return redirect(url_for("routes.add_investor"))
            else:
                return "При добавлении произошла ошибка"
        else:
            return render_template("add_investor.html")


@bp.route("/update_investor/<string:investor_name_old>", methods=["POST", "GET"])
def update_investor(investor_name_old):
    if request.method == "POST":
        with Session(engine) as session:
            investor_name_new = request.form["investor_name_new"]
            if investor_name_new == "":
                return "Пустой символ в имени инвестора"
            res = db_manager.update_investor(
                session=session, investor_name_old=investor_name_old, investor_name_new=investor_name_new
            )
            if res:
                redirect(url_for("routes.investors"))
                return redirect(url_for("routes.investors"))
            else:
                return "Ошибка в изменении имени"
    else:
        return redirect(url_for("routes.investors"))


@bp.route("/add_team_to_investor/<string:investor_name>", methods=["GET", "POST"])
def add_team_to_investor(investor_name):
    with Session(engine) as session:
        if request.method == "POST":
                team_name = request.form["team_name"]
                if team_name == "":
                    return "Ошибка: введен пустой символ"
                res = db_manager.add_investor_team(
                    session=session, team_name=team_name,
                    investor_name=investor_name
                )
                if res:
                    teams_list = db_manager.get_teams(session=session)
                    return redirect(url_for("routes.add_team_to_investor", investor_name=investor_name))
                else:
                    "Ошибка в добавлении команды"
        else:
            teams_list = db_manager.get_teams(session=session)
            return render_template("add_team_to_investor.html", investor_name=investor_name, teams=teams_list)


@bp.route("/delete_team_in_investor/<string:team_name>",methods=["POST", "GET"])
def delete_team_in_investor(team_name):
    if request.method == "GET":
        with Session(engine) as session:
            res = db_manager.delete_team(session=session, team_name=team_name)
            if res:
                return redirect(url_for("routes.investors"))
            else:
                return "Ошибка в удалении команды"
    else:
        return redirect(url_for("routes.investors"))


@bp.route("/remove_team_in_investor/<string:team_name>/<string:investor_name>")
def remove_team_in_investor(team_name, investor_name):
    if request.method == "GET":
        with Session(engine) as session:
            res = db_manager.remove_team_investor(session=session, team_name=team_name, investor_name=investor_name)
            if res:
                return redirect(url_for("routes.investors"))
            else:
                return "Ошибка в удалении связи команды и инвестора"
    else:
        return redirect(url_for("routes.investors"))


@bp.route("/update_team_to_investor/<string:team_name_old>", methods=["POST", "GET"])
def update_team_to_investor(team_name_old):
    if request.method == "POST":
        with Session(engine) as session:
            team_name_new = request.form["team_name_new"]
            if team_name_new == "":
                return "Ошибка введен пустой символ"
            res = db_manager.update_team(session=session, team_name_new=team_name_new, team_name_old=team_name_old)
            if res:
                return redirect(url_for("routes.investors"))
            else:
                return "Ошибка входных данных"
    else:
        return redirect(url_for("routes.investors"))


@bp.route("/remove_investor/<string:investor_name>")
def remove_investor(investor_name):
    with Session(engine) as session:
        if request.method == "GET":
            res = db_manager.remove_investor(investor_name=investor_name, session=session)
            if res:
                return redirect(url_for("routes.investors"))
            else:
                return "Ошибка в удалении игрока"
        else:
            return redirect(url_for("routes.investors"))


@bp.route("/players")
def players():
    with Session(engine) as session:
        players_list = db_manager.get_players(session=session)
        teams_list = db_manager.get_teams(session=session)
        for i in players_list:
            print(i.player_name)
        return render_template("players.html", players=players_list, teams=teams_list)


@bp.route("/add_player", methods=["POST", "GET"])
def add_player():
    with Session(engine) as session:
        if request.method == "POST":
            player_name = request.form["player_name"]
            if player_name == "":
                return "Введите имя игрока"
            res = db_manager.create_player(player_name=player_name, session=session)
            if res:
                return redirect(url_for("routes.add_player"))
            else:
                return "При добавлении произошла ошибка"
        else:
            teams_list = db_manager.get_teams(session=session)
            return render_template("add_player.html", teams=teams_list)


@bp.route("/update_player/<string:player_name_old>", methods=["POST", "GET"])
def update_player(player_name_old):
    with Session(engine) as session:
        if request.method == "POST":
            player_name_new = request.form["player_name_new"]
            team_name_new = request.form["team_name_new"]
            res = db_manager.update_player(
                player_name_old=player_name_old, player_name_new=player_name_new,
                team_name=team_name_new, session=session
            )
            if res:
                return redirect(url_for("routes.players"))
            else:
                return "Ошибка входных данных"
        else:
            return redirect(url_for("routes.players"))


@bp.route("/update_player_in_team/<string:player_name_old>", methods=["POST", "GET"])
def update_player_in_team(player_name_old):
    with Session(engine) as session:
        if request.method == "POST":
            player_name_new = request.form["player_name_new"]
            res = db_manager.update_player_without_team(
                player_name_old=player_name_old, player_name_new=player_name_new, session=session
            )
            if res:
                return redirect(url_for("routes.teams"))
            else:
                return "Ошибка входных данных"
        else:
            return redirect(url_for("routes.teams"))


@bp.route("/remove_player/<string:player_name>", methods=["POST", "GET"])
def remove_player(player_name):
    with Session(engine) as session:
        if request.method == "GET":
            res = db_manager.remove_player(player_name=player_name, session=session)
            if res:
                return redirect(url_for("routes.players"))
            else:
                return "Ошибка в удалении игрока"
        else:
            return redirect(url_for("routes.players"))


@bp.route("/remove_player_in_team/<string:player_name>", methods=["POST", "GET"])
def remove_player_in_team(player_name):
    with Session(engine) as session:
        if request.method == "GET":
            res = db_manager.remove_player(player_name=player_name, session=session)
            if res:
                return redirect(url_for("routes.teams"))
            else:
                return "Ошибка в удалении игрока"
        else:
            return redirect(url_for("routes.teams"))


@bp.route("/teams")
def teams():
    with Session(engine) as session:
        teams_list = db_manager.get_teams(session=session)
        return render_template("teams.html", teams=teams_list)


@bp.route("/add_team", methods=["POST", "GET"])
def add_team():
    with Session(engine) as session:
        if request.method == "POST":
            team_name = request.form["team_name"]
            if team_name == "":
                return "Введите название команды"
            res = db_manager.create_team(team_name=team_name, session=session)
            if res:
                return redirect(url_for("routes.add_team"))
            else:
                return "При добавлении произошла ошибка"
        else:
            return render_template("add_team.html")


@bp.route("/remove_team/<string:team_name>", methods=["POST", "GET"])
def remove_team(team_name):
    with Session(engine) as session:
        if request.method == "GET":
            res = db_manager.remove_team(team_name=team_name, session=session)
            if res:
                return redirect(url_for("routes.teams"))
            else:
                return "Ошибка в удалении игрока"
        else:
            return redirect(url_for("routes.teams"))


@bp.route("/update_team/<string:team_name>", methods=["GET", "POST"])
def update_team(team_name):
    if request.method == "POST":
        with Session(engine) as session:
            team_name_new = request.form["team_name_new"]
            res = db_manager.update_team(session=session, team_name_new=team_name_new, team_name_old=team_name)
            if res:
                return redirect(url_for("routes.teams"))
            else:
                return "Ошибка входных данных"
    else:
        return redirect(url_for("routes.teams"))


@bp.route("/add_player_in_team/<string:team_name>", methods=["GET", "POST"])
def add_player_in_team(team_name):
    if request.method == "POST":
        with Session(engine) as session:
            player_name = request.form["player_name"]
            res = db_manager.update_player(
                session=session, team_name=team_name,
                player_name_old=player_name, player_name_new=player_name
            )
            if res:
                return redirect(url_for("routes.teams", team_name=team_name))
    else:
        return render_template("add_player_in_team.html", team_name=team_name)


@bp.route("/update_investor_in_team/<string:investor_name_old>", methods=["GET", "POST"])
def update_investor_in_team(investor_name_old):
    if request.method == "POST":
        with Session(engine) as session:
            investor_name_new = request.form["investor_name_new"]
            if investor_name_new == "":
                return "Введен пустой символ"
            res = db_manager.update_investor(
                session=session, investor_name_new=investor_name_new, investor_name_old=investor_name_old
            )
            if res:
                return redirect(url_for("routes.teams"))
            else:
                return "Ошибка входных данных"
    else:
        return redirect(url_for("routes.teams"))


@bp.route("/remove_investor_in_team/<string:investor_name>", methods=["GET", "POST"])
def remove_investor_in_team(investor_name):
    with Session(engine) as session:
        if request.method == "GET":
            res = db_manager.remove_investor(investor_name=investor_name, session=session)
            if res:
                return redirect(url_for("routes.teams"))
            else:
                return "Ошибка в удалении инвестора"
        else:
            return redirect(url_for("routes.teams"))