"""add loglevel

Revision ID: 1135ee9863f9
Revises: 515e11f8acd8
Create Date: 2025-01-23 17:34:24.497592

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "1135ee9863f9"
down_revision: Union[str, None] = "515e11f8acd8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # まず、ENUM型を作成
    loglevel = postgresql.ENUM("DEBUG", "INFO", "ERROR", name="loglevel")
    loglevel.create(op.get_bind())

    # その後、カラムを追加
    op.add_column(
        "main_logs",
        sa.Column(
            "level",
            postgresql.ENUM("DEBUG", "INFO", "ERROR", name="loglevel"),
            nullable=False,
            server_default="INFO",
        ),
    )


def downgrade() -> None:
    # カラムを削除
    op.drop_column("main_logs", "level")

    # ENUM型を削除
    loglevel = postgresql.ENUM("DEBUG", "INFO", "ERROR", name="loglevel")
    loglevel.drop(op.get_bind())
