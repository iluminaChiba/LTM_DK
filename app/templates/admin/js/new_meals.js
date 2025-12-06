document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("new-meals-form");
  const tokenValue = form.dataset.token;

  const submitBtn = document.getElementById("register-all");

  submitBtn.addEventListener("click", () => {

    const hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.name = "token";
    hidden.value = tokenValue;
    form.appendChild(hidden);

    form.submit();
  });

});
