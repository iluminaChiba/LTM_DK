document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("pdfFile");
    const previewBtn = document.getElementById("run-preview");
    const commitBtn = document.getElementById("run-commit");
    const previewArea = document.getElementById("previewArea");

    // プレビュー処理
    previewBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];

        if (!file) {
            alert("PDFファイルを選択してください。");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        previewArea.textContent = "解析中です...\n";

        try {
            const res = await fetch("/api/admin/allergy_admin/upload", {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                previewArea.textContent = `エラー: ${res.status}`;
                return;
            }

            const data = await res.json();

            // 可読性のため整形して表示
            previewArea.textContent = JSON.stringify(data, null, 2);

        } catch (err) {
            previewArea.textContent = `通信エラー: ${err}`;
        }
    });

    // DB 反映
    commitBtn.addEventListener("click", async () => {
        if (!confirm("このデータをDBに登録しますか？")) return;

        try {
            const res = await fetch("/api/admin/allergy_admin/confirm", {
                method: "POST"
            });

            const data = await res.json();

            previewArea.textContent = JSON.stringify(data, null, 2);

            alert("DB登録が完了しました。");

        } catch (err) {
            previewArea.textContent = `通信エラー: ${err}`;
        }
    });
});
