from typing import TYPE_CHECKING

from . import Base
from .match_team import match_team

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .team import Team


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    points_team_1: Mapped[int]
    points_team_2: Mapped[int]
    teams: Mapped[list["Team"]] = relationship(back_populates="matches", secondary=match_team)
