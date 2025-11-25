import qrcode

def make_qr(url: str, output_path: str):
    img = qrcode.make(url)
    img.save(output_path)
    print(f"QR saved to: {output_path}")

if __name__ == "__main__":
    # ★ ここにあなたの token を貼る
    token = "00150ab62adc68c92f2c957ab69b09653748b9639ac3f4c155f3afde6ba081ac"

    base = "http://192.168.1.61:8000/api/entry/"
    url = f"{base}{token}/lunch"

    make_qr(url, "person_81.png")
