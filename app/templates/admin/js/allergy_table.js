const commitSubmitBtn = document.getElementById("commit-submit");
const registerActionBtn = document.getElementById("register-action");

commitSubmitBtn.addEventListener("click", async () => {
  if (!confirm("このデータをDBに登録しますか？")) return;

  // ボタンを無効化して二重送信を防止
  commitSubmitBtn.disabled = true;
  const originalText = commitSubmitBtn.textContent;
  commitSubmitBtn.textContent = "登録中...";

  try {
    // data-token属性からtokenを取得
    const token = commitSubmitBtn.dataset.token;
    if (!token) {
      alert("トークンが見つかりません。");
      return;
    }

    const res = await fetch(`/api/admin/allergy_admin/confirm/${token}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });

    const data = await res.json();

    if (res.ok) {
      // 成功時の詳細メッセージ
      let message = "アレルギー情報の登録が完了しました。\n\n";
      message += `新規追加: ${data.new_allergies?.length || 0}件\n`;
      message += `更新: ${data.updated_allergies?.length || 0}件\n`;
      message += `変更なし: ${data.unchanged_allergies?.length || 0}件\n`;

      if (data.new_meal_ids && data.new_meal_ids.length > 0) {
        message += `\n⚠️ 新規メニュー: ${data.new_meal_ids.length}件\n`;
        message += "「新規メニューの登録へ」ボタンから登録してください。";
      }

      alert(message);
    } else {
      alert("エラー: " + (data.detail || JSON.stringify(data)));
    }

  } catch (err) {
    alert("通信エラー: " + err.message);
  } finally {
    // ボタンを再度有効化
    commitSubmitBtn.disabled = false;
    commitSubmitBtn.textContent = originalText;
  }
});

registerActionBtn?.addEventListener("click", () => {
  const token = registerActionBtn.dataset.token;
  if (token) {
    window.location.href = `/api/admin/allergy_admin/new-meals/${token}`;
  }
});
