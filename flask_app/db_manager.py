from __future__ import annotations

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from sqlalchemy import select

from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from .models import Base
from .models import Investor
from .models import Match
from .models import Player
from .models import Team
from .models import investor_team


def create_bd():
    engine = create_engine(
        url=SQLALCHEMY_URL,
        echo=SQLALCHEMY_ECHO,
    )
    Base.metadata.create_all(bind=engine)


def create_investor(session: Session, investor_name: str) -> bool:
    investor = Investor()
    investor.investor_name = investor_name
    try:
        session.add(investor)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def get_investors(session: Session) -> list[Investor]:
    stmt = select(Investor).order_by(Investor.id)
    result: Result = session.execute(stmt)
    investors_list = result.scalars().all()
    return list(investors_list)


def remove_investor(session: Session, investor_name) -> bool:
    stmt = select(Investor).where(Investor.investor_name == investor_name)
    investor = session.scalar(stmt)
    try:
        session.delete(investor)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def update_investor(session: Session, investor_name_old: str, investor_name_new: str) -> bool:
    stmt = select(Investor).where(Investor.investor_name == investor_name_old)
    investor: Investor = session.scalar(stmt)
    investor.investor_name = investor_name_new
    try:
        session.add(investor)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def add_investor_team(session: Session, team_name: str, investor_name: str) -> bool:
    stmt = select(Investor).where(Investor.investor_name == investor_name)
    investor = session.scalar(stmt)
    stmt = select(Team).where(Team.team_name == team_name)
    team = session.scalar(stmt)
    conn_investor_team(investor=investor, team=team)
    try:
        session.add(investor)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def conn_investor_team(investor: Investor, team: Team):
    if investor.teams is None:
        investor.teams = list(team)
    elif team in investor.teams:
        pass
    else:
        investor.teams.append(team)


def get_matches(session: Session) -> list[Match]:
    stmt = select(Match)
    result: Result = session.execute(stmt)
    matches_list = result.scalars().all()
    return list(matches_list)


def create_match(
        points_team_1: int, points_team_2: int,
        team_name_1: str, team_name_2: str,
        match_name: str, session: Session,
) -> bool:
    team_1 = get_team(session=session, team_name=team_name_1)
    team_2 = get_team(session=session, team_name=team_name_2)
    if team_1 and team_2:
        match = Match()
        match.match_name = match_name
        match.teams = [team_1, team_2]
        match.points_team_1 = points_team_1
        match.points_team_2 = points_team_2
        session.add(match)
        session.commit()
        return True
    else:
        return False


def remove_match(session: Session, match_name: str) -> bool:
    stmt = select(Match).where(Match.match_name == match_name)
    match = session.scalar(stmt)
    try:
        session.delete(match)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def update_match(
        session: Session, match_name_old: str, match_name_new: str, team_1_name_new: str,
        team_2_name_new: str, points_1_new: int, points_2_new: int
) -> bool:
    stmt = select(Match).where(Match.match_name == match_name_old)
    match: Match = session.scalar(stmt)

    stmt = select(Team).where(Team.team_name == team_1_name_new)
    team_1: Team = session.scalar(stmt)
    if team_1 is None:
        return False

    stmt = select(Team).where(Team.team_name == team_2_name_new)
    team_2: Team = session.scalar(stmt)
    if team_2 is None:
        return False

    match.match_name = match_name_new
    match.points_team_1 = points_1_new
    match.points_team_2 = points_2_new
    match.teams = [team_2, team_1]
    try:
        session.add(match)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def get_players(session: Session) -> list[Player]:
    stmt = select(Player).order_by(Player.id)
    result: Result = session.execute(stmt)
    players_list = result.scalars().all()
    return list(players_list)


def create_player(player_name: str, session: Session) -> bool:
    player = Player()
    player.player_name = player_name

    try:
        session.add(player)
    except:
        session.rollback()
        return
    else:
        session.commit()
        return True


def update_player(player_name_old: str, session: Session, team_name: str, player_name_new: str) -> bool:
    stmt = select(Player).where(Player.player_name == player_name_old)
    player: Player = session.scalar(stmt)

    if player is None:
        return False
    if team_name == "":
        player.team = None
    elif player.team is None or player.team.team_name != team_name:
        stmt = select(Team).where(Team.team_name == team_name)
        team: Team = session.scalar(stmt)

        if team and player_name_new != "":
            conn_player_team(player=player, team=team)
        else:
            return False

    player.player_name = player_name_new
    try:
        session.add(player)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def update_player_without_team(player_name_old: str, session: Session, player_name_new: str) -> bool:
    stmt = select(Player).where(Player.player_name == player_name_old)
    player: Player = session.scalar(stmt)
    player.player_name = player_name_new
    try:
        session.add(player)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def conn_player_team(player: Player, team: Team):
    player.team = team
    player.team_id = team.id


def remove_player(player_name: str, session: Session) -> bool:
    stmt = select(Player).where(Player.player_name == player_name)
    player = session.scalar(stmt)
    try:
        session.delete(player)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def create_team(session: Session, team_name: str):
    team = Team()
    team.team_name = team_name
    try:
        session.add(team)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def delete_team(session: Session, team_name: str) -> bool:
    team = get_team(session=session, team_name=team_name)
    try:
        for match in team.matches:
            session.delete(match)
        session.delete(team)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def remove_team_investor(session: Session, team_name: str, investor_name: str) -> bool:
    team: Team = get_team(session=session, team_name=team_name)
    stmt = select(Investor).where(Investor.investor_name == investor_name)
    investor: Investor = session.scalar(stmt)
    stmt = delete(investor_team).where(investor_team.c.team_id == team.id, investor_team.c.investor_id == investor.id)
    try:
        session.execute(stmt)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True


def remove_team_player(session: Session, player_name: str) -> bool:
    stmt = select(Player).where(Player.player_name == player_name)
    player: Player = session.scalar(stmt)
    player.team = None
    try:
        session.add(player)
    except:
        session.rollback()
        return False
    else:
        session.commit()
        return True



def update_team(session: Session, team_name_old: str, team_name_new: str) -> bool:
    if team_name_new != "":
        team: Team = get_team(team_name=team_name_old, session=session)
        team.team_name = team_name_new
        try:
            session.add(team)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True
    else:
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
