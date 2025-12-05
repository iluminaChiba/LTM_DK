const commitSubmitBtn = document.getElementById("commit-submit");
const registerActionBtn = document.getElementById("register-action");

commitSubmitBtn.addEventListener("click", async () => {
  if (!confirm("このデータをDBに登録しますか？")) return;

  try {
    const res = await fetch("/api/admin/allergy_admin/commit", {
      method: "POST"
    });

    const data = await res.json();

    // 正常系
    if (res.ok) {
      alert("登録が完了しました。");
    } else {
      alert("エラー: " + JSON.stringify(data));
    }

  } catch (err) {
    alert("通信エラー: " + err);
  }
});

registerActionBtn?.addEventListener("click", () => {
  window.location.href = `/admin/allergy_admin/new-meals/${window.allergyToken}`;
});
