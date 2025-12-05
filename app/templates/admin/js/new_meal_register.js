// --------------------------------------------------
// 新規メニュー登録：同期確定処理 register-submit
// --------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    const registerBtn = document.getElementById("register-submit");
    const tableBody = document.getElementById("new-meal-rows");

    if (!registerBtn || !tableBody) return;

    registerBtn.addEventListener("click", async () => {
        if (!confirm("入力内容をDBに登録しますか？")) return;

        // ----------------------------
        // 入力されたデータを収集（JSON配列化）
        // ----------------------------
        const items = [];

        tableBody.querySelectorAll("tr").forEach(row => {
            const mealId = row.dataset.mealId;

            const mealName = row.querySelector(".meal-name")?.value.trim() || "";
            const furigana = row.querySelector(".furigana")?.value.trim() || "";

            const kcal = row.querySelector(".kcal")?.value || null;
            const protein = row.querySelector(".protein")?.value || null;
            const fat = row.querySelector(".fat")?.value || null;
            const carb = row.querySelector(".carb")?.value || null;
            const salt = row.querySelector(".salt")?.value || null;

            items.push({
                meal_id: mealId,
                meal_name: mealName,
                furigana: furigana,
                kcal: kcal ? Number(kcal) : null,
                protein: protein ? Number(protein) : null,
                fat: fat ? Number(fat) : null,
                carb: carb ? Number(carb) : null,
                salt: salt ? Number(salt) : null
            });
        });

        // 必須チェック（ meal_name が空の場合）
        const missingName = items.find(item => !item.meal_name);
        if (missingName) {
            alert("未入力の正式名称があります。全ての行の名前を入力してください。");
            return;
        }

        // ----------------------------
        // API に JSON を送信
        // ----------------------------
        try {
            const res = await fetch("/api/admin/allergy_admin/new-meals/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ items })
            });

            const data = await res.json();

            if (!res.ok) {
                alert("エラーが発生しました。\n" + JSON.stringify(data, null, 2));
                return;
            }

            // ----------------------------
            // 成功時（自動遷移はしない）
            // ----------------------------
            alert("新規メニューの登録が完了しました。");

        } catch (err) {
            alert("通信エラー: " + err);
        }
    });
});
