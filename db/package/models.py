from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text

from .connection import Base


class LogLevel(int, Enum):
    DEBUG = 10
    INFO = 20
    ERROR = 30

    @classmethod
    def from_str(cls, level: str) -> "LogLevel":
        level_map = {
            "DEBUG": cls.DEBUG,
            "INFO": cls.INFO,
            "ERROR": cls.ERROR,
        }
        return level_map.get(level.upper(), cls.INFO)

    @classmethod
    def from_int(cls, level: int) -> "LogLevel":
        level_map = {
            10: cls.DEBUG,
            20: cls.INFO,
            30: cls.ERROR,
        }
        return level_map.get(level, cls.INFO)

    def __str__(self) -> str:
        return self.name


class MainLog(Base):
    __tablename__ = "main_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    app_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=20, index=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
