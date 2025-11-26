import qrcode

def make_qr(url: str, output_path: str):
    img = qrcode.make(url)
    img.save(output_path)
    print(f"QR saved to: {output_path}")

if __name__ == "__main__":
    # ここにテスト用のtokenを貼る
    token = "481fea609cb3e0f0215c1751b61122c8725e8c00634daafb9795c4390402c313"

    base = "http://192.168.1.61:8000/frontend/ui_test.html?token="
    url = f"{base}{token}"

    make_qr(url, "person_83.png")
