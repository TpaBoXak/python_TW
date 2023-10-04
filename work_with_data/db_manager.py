from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from tabel import Base
from tabel import Investor


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
