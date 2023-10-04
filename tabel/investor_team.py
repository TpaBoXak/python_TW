from tabel.base import Base

from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column


investor_team = Table(
    "investor_team",
    Base.metadata,
    Column("investor_id", ForeignKey("investors.id")),
    Column("team_id", ForeignKey("teams.id")),
)
