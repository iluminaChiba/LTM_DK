def load_csv_as_matrix(path: str) -> list[list[str]]:
    """
    生CSVを二次元配列（list[list[str]]]）として読み込む。
    空行は飛ばす。
    """
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(line.split(","))
    return rows


def marker_to_bool(cell: str) -> bool:
    """
    セル値を bool に変換する。
    ● -> True、それ以外 -> False
    """
    return cell == "●"


def convert_matrix_to_bool(rows: list[list[str]]) -> list[list[bool]]:
    """
    文字列行列（CSV読み込み結果）を boolean 行列へ。
    """
    bool_rows = []
    for row in rows:
        bool_row = [marker_to_bool(cell) for cell in row]
        bool_rows.append(bool_row)
    return bool_rows
