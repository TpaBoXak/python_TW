from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from tabel import Base
from tabel import Investor
from tabel import Match
from tabel import Player
from tabel import Team


engine = create_engine(
    url=SQLALCHEMY_URL,
    echo=SQLALCHEMY_ECHO,
)

session = Session(engine)


def create_bd():
    Base.metadata.create_all(bind=engine)


def create_investor():
    investor = Investor()
    session.add(investor)
    session.commit()


def create_match():
    match = Match()
    session.add(match)
    session.commit()


def create_player():
    player = Player()
    session.add(player)
    session.commit()


def create_team():
    team = Team()
    session.add(team)
    session.commit()
