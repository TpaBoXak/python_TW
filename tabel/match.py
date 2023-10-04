from typing import TYPE_CHECKING

from tabel.base import Base
from tabel.match_team import match_team

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .team import Team


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped
    teams: Mapped[list["Team"]] = relationship(back_populates="matches", secondary=match_team)
