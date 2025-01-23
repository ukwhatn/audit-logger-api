from fastapi import APIRouter

from .root import main as root_router
from .admin import main as admin_router

# define router
router = APIRouter()

# add routers
router.include_router(root_router.router)
router.include_router(admin_router.router)
