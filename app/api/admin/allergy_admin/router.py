from fastapi import APIRouter

from .preview import router as preview_router
from .confirm import router as confirm_router
from .new_meal_ui import router as new_meal_ui_router
from .table_view import router as table_view_router

router = APIRouter()

router.include_router(preview_router, prefix="",)
router.include_router(confirm_router, prefix="")
router.include_router(new_meal_ui_router)
router.include_router(table_view_router)