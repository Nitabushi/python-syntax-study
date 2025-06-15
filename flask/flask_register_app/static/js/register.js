const form = document.getElementById("register-form");
const inputs = document.querySelectorAll("input");
const submitBtn = document.getElementById("submit-btn");

function validateForm() {
  let allFilled = true;
  inputs.forEach(input => {
    if (input.type !== "hidden" && input.value.trim() === "") {
      allFilled = false;
    }
  });
  submitBtn.disabled = !allFilled;
}

inputs.forEach(input => {
  input.addEventListener("input", validateForm);
});

window.addEventListener("DOMContentLoaded", validateForm);

form.addEventListener("submit", function(event) {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const message = `以下の内容で登録してよろしいですか？\n\n` +
                  `ユーザー名: ${username}\n` +
                  `メールアドレス: ${email}\n` +
                  `パスワード: ${'*'.repeat(password.length)}`;

  if (!confirm(message)) {
    event.preventDefault();
  }
});
