// Excel Order - Upload & Preview
const previewActionBtn = document.getElementById("preview-action");
const registerActionBtn = document.getElementById("register-action");

previewActionBtn.addEventListener("click", async () => {
  const fileInput = document.getElementById("excelFile");
  if (!fileInput.files.length) {
    alert("ファイルを選んでください");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("/api/admin/excel_order/upload", {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    document.getElementById("previewArea").textContent =
      "エラー: " + res.status + " " + (await res.text());
    return;
  }

  const result = await res.json();
  window.previewData = result.preview;
  window.token = result.token;

  // 画面表示
  document.getElementById("previewArea").textContent =
    JSON.stringify(window.previewData, null, 2);

  // 本登録ボタンを有効化
  goRegisterBtn.disabled = false;
});

registerActionBtn.addEventListener("click", async () => {
  if (!window.token) {
    alert("トークンがありません。先にプレビューを実行してください。");
    return;
  }

  window.location.href = `/api/admin/excel_order/register/${window.token}`;
});