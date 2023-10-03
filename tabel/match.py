from typing import TYPE_CHECKING

from tabel.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .team import Team


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)

    team_1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team_1: Mapped["Team"] = relationship(back_populates="Matches")

    team_2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team_2: Mapped["Team"] = relationship(back_populates="Matches")
