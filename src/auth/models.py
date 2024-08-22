from datetime import datetime, timezone

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import (
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.now(timezone.utc)),
    Column("role_id", Integer, ForeignKey("roles.id")),
)
