from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Response
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.package.crud.main_log import create as log_create
from db.package.session import db_context
from util.env import get_api_keys

# define router
router = APIRouter()

APP_KEYS = get_api_keys("APP_API_KEYS")
if not APP_KEYS or len(APP_KEYS) == 0:
    raise Exception("No app api keys found")

app_name_header = APIKeyHeader(name="X-AppName", auto_error=True)
app_key_header = APIKeyHeader(name="X-AppKey", auto_error=True)


def check_app_key(name: str, key: str):
    return name in APP_KEYS and APP_KEYS[name] == key


# define route
class CreateLogRequestSchema(BaseModel):
    app_name: str
    action: str
    message: str
    notes: str | None = None
    ip_address: str | None = None


class CreateLogResponseSchema(BaseModel):
    message: str


@router.post("/logging", response_model=CreateLogResponseSchema)
def create_log(
        request: Request,
        response: Response,
        data: CreateLogRequestSchema,
        db: Session = Depends(db_context),
        app_name: str = Depends(app_name_header),
        app_key: str = Depends(app_key_header)
):
    # authenticate
    if not check_app_key(app_name, app_key):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # validate
    if data.app_name != app_name:
        raise HTTPException(status_code=400, detail="Invalid app name")

    # create log
    log_create(
        db,
        data.app_name,
        data.action,
        data.message,
        data.notes,
        data.ip_address
    )
    response.status_code = 201
    return {"message": "Log created"}
