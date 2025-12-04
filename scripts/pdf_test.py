import pdfplumber

PDF_PATH = "scripts/test.pdf"  # Dockerコンテナ内では /workspace がカレントディレクトリ

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[0]
    words = page.extract_words()

    print(f"総抽出単語数: {len(words)}")
    print("=== 先頭 40 個の raw 座標データ ===")

    for w in words[:40]:
        print(w)
