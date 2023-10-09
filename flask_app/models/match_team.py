from . import Base

from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column


match_team = Table(
    "match_team",
    Base.metadata,
    Column("match_id", ForeignKey("matches.id")),
    Column("team_id", ForeignKey("teams.id")),
)
