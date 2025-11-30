window.onload = () => {
  const btn = document.getElementById("submit-btn");

  btn.onclick = async () => {
    const inputs = document.querySelectorAll(".qty-input");

    const orders = [];
    inputs.forEach(inp => {
      const mealId = inp.dataset.mealId;
      const raw = inp.value.trim();

      orders.push({
        meal_id: mealId,
        qty: raw === "" ? null : Number(raw),
      });
    });

    const res = await fetch("/api/order/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: document.querySelector("p").innerText,
        orders: orders
      })
    });

    if (res.ok) {
      alert("発注を登録しました。pending_importへ保存しました！");
    } else {
      alert("登録に失敗しました。");
    }
  };
};
