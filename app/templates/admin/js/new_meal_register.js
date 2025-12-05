document.getElementById("submit-btn").addEventListener("click", async () => {

  const formEl = document.getElementById("meal-register-form");
  const formData = new FormData(formEl);

  // FormData → JSON 化
  const payload = { items: [] };
  const indexSet = new Set();

  for (let [key, value] of formData.entries()) {
      const match = key.match(/items\[(\d+)\]\[(.+)\]/);
      if (!match) continue;

      const idx = match[1];
      const field = match[2];
      indexSet.add(idx);

      if (!payload.items[idx]) payload.items[idx] = {};
      payload.items[idx][field] = value;
  }

  // 数値変換（空欄は除外）
  payload.items = payload.items.map(item => {
      ["kcal","protein","fat","carb","salt"].forEach(f => {
          // item[f]が存在する場合のみ処理 (シンプル化のため元のロジックを維持)
          if (item.hasOwnProperty(f) && item[f] === "") delete item[f];
          else if (item.hasOwnProperty(f)) item[f] = parseFloat(item[f]);
      });
      item.meal_id = parseInt(item.meal_id);
      return item;
  }).filter(item => item.meal_id); // meal_id がある行のみフィルタ

  // ⚠️ FastAPI のエンドポイントに合わせて修正 ⚠️
  // FastAPI + APIRouter の構成を考慮し、/admin/meals/bulk が正しいと仮定
  const res = await fetch("/admin/meals/bulk", { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
  });

  if (res.ok) {
      alert("メニューを登録しました。");
      location.reload();
  } else {
      const err = await res.json();
      alert("エラー: " + err.detail);
  }
});