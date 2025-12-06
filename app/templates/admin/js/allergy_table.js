// app/static/js/allergy_table.js
document.addEventListener("DOMContentLoaded", () => {

  const commitBtn = document.getElementById("commit-submit");
  const registerBtn = document.getElementById("register-action");

  // -------------------------------------------------------
  // DB登録（画面遷移方式）
  // -------------------------------------------------------
  if (commitBtn) {
    commitBtn.addEventListener("click", () => {

      const token = commitBtn.dataset.token;
      if (!token) {
        alert("トークンが取得できません。");
        return;
      }

      if (!confirm("このデータを DB に登録しますか？")) {
        return;
      }

      // 通常の POST 画面遷移
      const form = document.createElement("form");
      form.method = "POST";
      form.action = `/api/admin/allergy_admin/confirm/${token}`;
      document.body.appendChild(form);
      form.submit();
    });
  }

  // -------------------------------------------------------
  // 新規メニュー登録画面へ
  // -------------------------------------------------------
  if (registerBtn) {
    registerBtn.addEventListener("click", () => {

      const token = registerBtn.dataset.token;
      if (!token) {
        alert("トークンが取得できません。");
        return;
      }

      window.location.href = `/api/admin/allergy_admin/new_meals/${token}`;
    });
  }

});
