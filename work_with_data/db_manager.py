from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from sqlalchemy import select

from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from tabel import Base
from tabel import Investor
from tabel import Match
from tabel import Player
from tabel import Team


def create_bd():
    engine = create_engine(
        url=SQLALCHEMY_URL,
        echo=SQLALCHEMY_ECHO,
    )
    Base.metadata.create_all(bind=engine)


def create_investor(session: Session):
    investor = Investor()
    session.add(investor)
    session.commit()


def create_match(score: str, session: Session):
    match = Match()
    if score is None:
        score = "-:-"
    match.score = score
    session.add(match)
    session.commit()


def get_players(session: Session) -> list[Player]:
    stmt = select(Player).order_by(Player.id)
    players_list = []
    result: Result = session.execute(stmt)
    players_list = result.scalars().all()
    return list(players_list)


def create_player(player_name: str, team_name: str, session: Session) -> False | True:
    player = Player()
    player.player_name = player_name
    if team_name:
        team = get_team(session=session, team_name=team_name)
        if team:
            player.teams = team
            player.team_id = team.id
        else:
            return False
    try:
        session.add(player)
        session.commit()
        return True
    except:
        return False


def create_team(session: Session):
    team = Team()
    session.add(team)
    session.commit()


def get_teams(session: Session) -> list[Team]:
    stmt = select(Team).order_by(Team.id)
    teams_list = []
    result: Result = session.execute(stmt)
    teams_list = result.scalars().all()
    return list(teams_list)


def get_team(team_name: str, session: Session) -> Team | None:
    stmt = select(Team).where(Team.team_name == team_name)
    team: Team | None = session.scalar(stmt)
    return team

# create_bd()
# create_player("Bob")
# create_player("Steave")
# create_player("John")
# create_player("Pop")


# players = get_players()
# for player in players:
#     print(player.id + player.player_name)