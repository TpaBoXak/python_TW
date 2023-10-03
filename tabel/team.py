from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from tabel.base import Base


if TYPE_CHECKING:
    from .investor import Investor
    from .match import Match
    from .player import Player


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    investors: Mapped[list["Investor"]] = relationship(back_populates="team")
    matches: Mapped[list["Match"]] = relationship(back_populates="team")
    players: Mapped[list["Player"]] = relationship(back_populates="team")
