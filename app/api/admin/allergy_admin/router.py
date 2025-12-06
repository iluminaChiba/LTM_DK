from fastapi import APIRouter

from .preview import router as preview_router
from .confirm import router as confirm_router
from .table_view import router as table_view_router
from .new_meals import router as new_meals_router

router = APIRouter()

router.include_router(preview_router, prefix="",)
router.include_router(confirm_router, prefix="")
router.include_router(table_view_router)
router.include_router(new_meals_router)