from typing import TYPE_CHECKING

from tabel.base import Base
from tabel.investor_team import investor_team

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String


if TYPE_CHECKING:
    from .team import Team


class Investor(Base):
    __tablename__ = "investors"

    id: Mapped[int] = mapped_column(primary_key=True)
    investor_name: Mapped[str] = mapped_column(String(30), unique=True)
    teams: Mapped[list["Team"]] = relationship(back_populates="investors", secondary=investor_team)
