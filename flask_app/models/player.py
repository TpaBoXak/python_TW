from typing import TYPE_CHECKING

from . import Base

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .team import Team


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=True)
    teams: Mapped["Team"] = relationship(back_populates="players")

    def __repr__(self):
        return f"<Player(id={self.id}, player_name='{self.player_name}', team_id={self.team_id})>"
