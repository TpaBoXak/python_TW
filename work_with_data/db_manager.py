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


def get_matches(session: Session):
    stmt = select(Match).order_by(Match.id)
    result: Result = session.execute(stmt)
    matches_list = result.scalars().all()
    return list(matches_list)


def create_match(
        points_team_1: int, points_team_2: int,
        team_name_1: int, team_name_2: int,
        session: Session,
    ) -> True | False:
    team_1 = get_team(session=session, team_name=team_name_1)
    team_2 = get_team(session=session, team_name=team_name_2)
    if team_1 and team_2:
        math = Match()
        math.teams = [team_1, team_2]
        math.points_team_1 = points_team_1
        math.points_team_2 = points_team_2
        session.add(math)
        session.commit()
        return True
    else:
        return False


def get_players(session: Session) -> list[Player]:
    stmt = select(Player).order_by(Player.id)
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


def create_team(session: Session, team_name: str):
    team = Team()
    team.team_name = team_name
    try:
        session.add(team)
        session.commit()
        return True
    except:
        return False


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