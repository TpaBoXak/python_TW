from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String

from . import Base
from .investor_team import investor_team
from .match_team import match_team


if TYPE_CHECKING:
    from .investor import Investor
    from .match import Match
    from .player import Player


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    investors: Mapped[list["Investor"]] = relationship(back_populates="teams", secondary=investor_team)
    matches: Mapped[list["Match"]] = relationship(back_populates="teams", secondary=match_team)
    players: Mapped[list["Player"]] = relationship(back_populates="team")


