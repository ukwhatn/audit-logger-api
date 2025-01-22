from datetime import datetime

from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text

from .connection import Base


class MainLog(Base):
    __tablename__ = "main_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    app_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )
    action: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    message: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    notes: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    ip_address: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()")
    )
