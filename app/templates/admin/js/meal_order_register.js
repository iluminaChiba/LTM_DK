document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("submit-btn");

  submitBtn.addEventListener("click", async () => {
    const rows = gatherRows();
    if (rows.length === 0) {
      alert("データがありません。");
      return;
    }

    console.log("[DEBUG] rows:", rows);

    try {
      const response = await fetch("/api/admin/excel_order/confirm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(rows),
      });

      if (!response.ok) {
        const err = await response.json();
        alert("登録に失敗しました：" + JSON.stringify(err));
        return;
      }

      const result = await response.json();
      alert(`登録しました。${result.message}`);

    } catch (error) {
      console.error(error);
      alert("通信エラーが発生しました。");
    }
  });
});


/**
 * テーブルから必要情報を抽出する
 */
function gatherRows() {
  const tbody = document.querySelector("body");

  const arrivalDate = tbody.dataset.arrivalDate;
  const applicableDate = tbody.dataset.applicableDate;
  const sourceFilename = tbody.dataset.sourceFilename;

  const rows = [];
  const trList = document.querySelectorAll("#order-table tbody tr");

  trList.forEach((tr) => {
    const excelRow = parseInt(tr.children[0].textContent.trim(), 10);
    const mealId = tr.children[1].textContent.trim();
    const mealName = tr.children[2].textContent.trim();
    const qtyInput = tr.querySelector("input.qty-input");

    const qty = qtyInput.value === "" ? 0 : parseInt(qtyInput.value, 10);

    rows.push({
      meal_id: mealId,
      meal_name: mealName === "" ? null : mealName,
      qty: qty,
      arrival_date: arrivalDate,
      applicable_date: applicableDate,
      source_filename: sourceFilename,
      excel_row: excelRow,
      status: "pending",
    });
  });

  return rows;
}
