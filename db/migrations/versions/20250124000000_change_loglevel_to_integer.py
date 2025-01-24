"""change loglevel to integer

Revision ID: change_loglevel_to_integer
Revises: 1135ee9863f9
Create Date: 2025-01-24 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "change_loglevel_to_integer"
down_revision: Union[str, None] = "1135ee9863f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 一時的な数値カラムを作成
    op.add_column("main_logs", sa.Column("level_int", sa.Integer(), nullable=True))

    # 既存のデータを変換
    op.execute("""
        UPDATE main_logs 
        SET level_int = CASE level
            WHEN 'DEBUG' THEN 10
            WHEN 'INFO' THEN 20
            WHEN 'ERROR' THEN 30
        END
    """)

    # 古いカラムを削除
    op.drop_column("main_logs", "level")

    # ENUMタイプを削除
    op.execute("DROP TYPE loglevel")

    # 新しいカラムをlevelにリネーム
    op.alter_column("main_logs", "level_int", new_column_name="level")

    # NOT NULL制約とデフォルト値を設定
    op.alter_column(
        "main_logs", "level", nullable=False, server_default="20", type_=sa.Integer()
    )

    # インデックスを作成
    op.create_index(op.f("ix_main_logs_level"), "main_logs", ["level"], unique=False)


def downgrade() -> None:
    # インデックスを削除
    op.drop_index(op.f("ix_main_logs_level"), table_name="main_logs")

    # ENUMタイプを作成
    loglevel = postgresql.ENUM("DEBUG", "INFO", "ERROR", name="loglevel")
    loglevel.create(op.get_bind())

    # 一時的な文字列カラムを作成
    op.add_column(
        "main_logs",
        sa.Column(
            "level_enum",
            postgresql.ENUM("DEBUG", "INFO", "ERROR", name="loglevel"),
            nullable=True,
        ),
    )

    # データを逆変換
    op.execute("""
        UPDATE main_logs 
        SET level_enum = CASE level
            WHEN 10 THEN 'DEBUG'
            WHEN 20 THEN 'INFO'
            WHEN 30 THEN 'ERROR'
        END::loglevel
    """)

    # 数値カラムを削除
    op.drop_column("main_logs", "level")

    # 新しいカラムをlevelにリネーム
    op.alter_column("main_logs", "level_enum", new_column_name="level")

    # NOT NULL制約とデフォルト値を設定
    op.alter_column(
        "main_logs",
        "level",
        nullable=False,
        server_default="'INFO'",
        type_=postgresql.ENUM("DEBUG", "INFO", "ERROR", name="loglevel"),
    )
