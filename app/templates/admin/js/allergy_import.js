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

        console.log("Selected file:", file.name, file.type, file.size);

        const formData = new FormData();
        formData.append("file", file);

        previewArea.textContent = "解析中です...\n";
        console.log("Sending request to /api/admin/allergy_admin/upload");

        try {
            const res = await fetch("/api/admin/allergy_admin/upload", {
                method: "POST",
                body: formData
            });

            console.log("Response status:", res.status);

            if (!res.ok) {
                const errorText = await res.text();
                console.error("Error response:", errorText);
                try {
                    const errorData = JSON.parse(errorText);
                    previewArea.textContent = `エラー: ${res.status}\n${JSON.stringify(errorData, null, 2)}`;
                } catch {
                    previewArea.textContent = `エラー: ${res.status}\n${errorText}`;
                }
                return;
            }

            const data = await res.json();
            console.log("Success data:", data);

            // 可読性のため整形して表示
            previewArea.textContent = JSON.stringify(data, null, 2);

        } catch (err) {
            console.error("Fetch error:", err);
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
