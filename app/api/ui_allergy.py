from fastapi import APIRouter
from app.utils.ui.allergy_loader import load_csv_as_matrix, convert_matrix_to_bool
from pathlib import Path

router = APIRouter()

@router.get("/")
def get_allergy_data():
    base = Path(__file__).resolve().parents[1] 
    csv_dir = base / "resources" / "allergies"

    # アレルギーマトリックスの読み込み
    raw_matrix = load_csv_as_matrix(str(csv_dir / "allergy_raw_2025_12.csv"))
    matrix = convert_matrix_to_bool(raw_matrix)
    
    # ラベルの読み込み（1行目をそのまま使う）
    labels_raw = load_csv_as_matrix(str(csv_dir / "labels.csv"))
    labels = labels_raw[0] if labels_raw else []

    return {
        "labels": labels,
        "matrix": matrix,
    }
