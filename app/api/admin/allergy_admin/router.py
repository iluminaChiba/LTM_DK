from fastapi import APIRouter

# 各機能ファイル（responsibility-based modules）
from .preview import router as preview_router
from .confirm import router as confirm_router

router = APIRouter()

# -------------------------
#  Allergy Importer Routes
#  (Excel importer と完全一致)
# -------------------------

# /api/admin/allergy_admin/import
# /api/admin/allergy_admin/upload
router.include_router(
    preview_router,
    prefix="",
)

# /api/admin/allergy_admin/confirm
router.include_router(
    confirm_router,
    prefix="",
)
