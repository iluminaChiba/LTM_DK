document.addEventListener("DOMContentLoaded", () => {

  const submitBtn = document.getElementById("submit-btn");

  submitBtn.addEventListener("click", async () => {

    // HTML body から日付情報を取得
    const arrivalDate = document.body.dataset.arrivalDate;
    const applicableDate = document.body.dataset.applicableDate;
    const sourceFilename = document.body.dataset.sourceFilename;

    console.log("[DEBUG] arrivalDate:", arrivalDate);
    console.log("[DEBUG] applicableDate:", applicableDate);
    console.log("[DEBUG] sourceFilename:", sourceFilename);

    // qty-input を全て取得
    const inputs = document.querySelectorAll(".qty-input");
    const tableRows = document.querySelectorAll("#order-table tbody tr");

    // 登録対象の行だけ抽出
    const payload = [];
    tableRows.forEach((tr) => {
      const excelRow = parseInt(tr.children[0].textContent.trim(), 10);
      const mealId = tr.children[1].textContent.trim();
      const mealName = tr.children[2].textContent.trim();
      const qtyInput = tr.querySelector("input.qty-input");
      const qty = qtyInput.value === "" ? 0 : parseInt(qtyInput.value, 10);

      if (qty > 0) {
        payload.push({
          meal_id: mealId,
          meal_name: mealName || null,
          qty: qty,
          arrival_date: arrivalDate,
          applicable_date: applicableDate,
          source_filename: sourceFilename,
          excel_row: excelRow,
          status: "pending"
        });
      }
    });

    if (payload.length === 0) {
      alert("数量が入力された行がありません。");
      return;
    }

    console.log("[DEBUG] payload:", JSON.stringify(payload, null, 2));

    // API へ送信
    const res = await fetch("/api/pending_box/bulk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errorText = await res.text();
      alert("登録に失敗しました: " + errorText);
      return;
    }

    const data = await res.json();
    console.log("登録結果:", data);

    alert(`${data.length}件をpending_boxへ登録しました！`);
  });
});
