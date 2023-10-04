from typing import TYPE_CHECKING

from tabel.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .team import Team


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=True)
    teams: Mapped["Team"] = relationship(back_populates="players")
