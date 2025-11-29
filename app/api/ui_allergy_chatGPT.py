from fastapi import APIRouter
from app.utils.ui.allergy_loader import load_allergy_bool_matrix
from app.utils.ui.allergy_loader import load_labels_csv  # 必要なら
from pathlib import Path

router = APIRouter()

@router.get("/ui/allergy")
def get_allergy_data():
    base = Path(__file__).resolve().parents[2]  # LTM_DK/app まで戻る
    csv_dir = base / "resources" / "allergies"

    matrix = load_allergy_bool_matrix(csv_dir / "allergy_raw_2025_12.csv")
    labels = load_labels_csv(csv_dir / "labels.csv")

    return {
        "labels": labels,
        "matrix": matrix,
    }
