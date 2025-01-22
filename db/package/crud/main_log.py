from typing import Type

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models import MainLog


def get(db: Session, main_log_id: int) -> MainLog | None:
    return db.query(MainLog).filter(MainLog.id == main_log_id).first()


def get_for_list(
        db: Session,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "created_at",
        order: str = "desc"
) -> tuple[list[Type[MainLog]], int]:
    all_data = db.query(MainLog)
    total = all_data.count()
    data = all_data.order_by(text(order_by + " " + order)).limit(per_page).offset((page - 1) * per_page).all()
    return data, total


def create(
        db: Session,
        app_name: str,
        action: str,
        message: str,
        notes: str | None = None,
        ip_address: str | None = None
) -> None:
    db.add(MainLog(
        app_name=app_name,
        action=action,
        message=message,
        notes=notes if notes != "" else None,
        ip_address=ip_address if ip_address != "" else None
    ))
    db.commit()

# ------
# Template
# ------

# def get(db: Session, note_id: int) -> models.Note | None:
#     return db.query(models.Note).filter(models.Note.id == note_id).first()
#
#
# def get_by_actor(db: Session, actor_id: int) -> list[models.Note]:
#     return db.query(models.Note).filter(models.Note.actor_id == actor_id).all()
#
#
# def get_by_actor_and_id(db: Session, actor_id: int, note_id: int) -> models.Note | None:
#     return db.query(models.Note).filter(models.Note.actor_id == actor_id, models.Note.id == note_id).first()
#
#
# def create(db: Session, note: schemas.NoteCreate) -> models.Note:
#     db_note = models.Note(
#         actor_id=note.actor_id,
#         title=note.title,
#         content=note.content
#     )
#     db.add(db_note)
#     db.commit()
#     db.refresh(db_note)
#     return db_note
