from datetime import datetime, timezone

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    Table,
)

from database import metadata

operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", Integer),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column(
        "date", TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
    ),
    Column("type", String),
)
