from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from tabel import Base


engine = create_engine(
    url=SQLALCHEMY_URL,
    echo=SQLALCHEMY_ECHO,
)


# class Base(DeclarativeBase):
#     pass
#
#
# class Investor(Base):
#     __tablename__ = "investors"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     teams: Mapped[list["Team"]] = relationship(back_populates="investors")
#
#
# class Match(Base):
#     __tablename__ = "matches"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#
#     team_1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
#     team_1: Mapped["Team"] = relationship(back_populates="Matches")
#
#     team_2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
#     team_2: Mapped["Team"] = relationship(back_populates="Matches")
#
#
# class Player(Base):
#     __tablename__ = "players"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
#     team: Mapped["Team"] = relationship(back_populates="players")
#
#
# class Team(Base):
#     __tablename__ = "teams"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     investors: Mapped[list["Investor"]] = relationship(back_populates="team")
#     matches: Mapped[list["Match"]] = relationship(back_populates="team")
#     players: Mapped[list["Player"]] = relationship(back_populates="team")


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Start")
    main()
