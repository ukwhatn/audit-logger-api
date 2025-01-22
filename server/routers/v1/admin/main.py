from datetime import datetime

from fastapi import APIRouter
from fastapi import Request, Response, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.package.crud.main_log import get_for_list as get_main_logs
from db.package.session import db_context
from util.env import get_api_keys

# define router
router = APIRouter()

ADMIN_KEYS = get_api_keys("ADMIN_API_KEYS")
if not ADMIN_KEYS or len(ADMIN_KEYS) == 0:
    raise Exception("No admin keys found")

admin_key_name = APIKeyHeader(name="X-AdminName", auto_error=True)
admin_key_header = APIKeyHeader(name="X-AdminKey", auto_error=True)


def check_admin_key(name: str, key: str):
    return name in ADMIN_KEYS and ADMIN_KEYS[name] == key


class GetListResponseSchema(BaseModel):
    class Child(BaseModel):
        app_name: str
        action: str
        message: str
        notes: str
        ip_address: str
        created_at: datetime

    data: list[Child]
    page: int
    per_page: int
    total: int

# define route
@router.get("/list", response_model=GetListResponseSchema)
async def get_list(
        request: Request,
        response: Response,
        admin_name: str = Depends(admin_key_name),
        admin_key: str = Depends(admin_key_header),
        db: Session = Depends(db_context),
        page: int = 1,
        per_page: int = 100,
        order_by: str = "created_at",
        order: str = "desc",
):
    # authenticate
    if not check_admin_key(admin_name, admin_key):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # validate
    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 1

    if order_by not in ["app_name", "action", "message", "notes", "ip_address", "created_at"]:
        order_by = "created_at"

    if order not in ["asc", "desc"]:
        order = "desc"

    # get data
    data, total = get_main_logs(db, page, per_page, order_by, order)

    # return
    return {
        "data": [
            {
                "app_name": datum.app_name,
                "action": datum.action,
                "message": datum.message,
                "notes": datum.notes,
                "ip_address": datum.ip_address,
                "created_at": datum.created_at
            } for datum in data
        ],
        "page": page,
        "per_page": per_page,
        "total": total
    }
