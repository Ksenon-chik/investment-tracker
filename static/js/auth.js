function showLogin() {
    document.getElementById("login-form").style.display = "block";
    document.getElementById("register-form").style.display = "none";
    document.getElementById("login-tab").classList.add("active");
    document.getElementById("register-tab").classList.remove("active");
}

function showRegister() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "block";
    document.getElementById("login-tab").classList.remove("active");
    document.getElementById("register-tab").classList.add("active");
}

async function handleRegister(event) {
    event.preventDefault();
    const form = event.target;
    const errorDiv = document.getElementById("js-error-msg");
    errorDiv.style.display = "none";

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    if (data.password !== data.confirm_password) {
        errorDiv.innerText = "Пароли не совпадают";
        errorDiv.style.display = "block";
        return;
    }

    data.start_balance = parseFloat(data.start_balance);
    delete data.confirm_password;

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/profile";
        } else {
            errorDiv.innerText = result.detail;
            errorDiv.style.display = "block";
        }
    } catch (err) {
        errorDiv.innerText = "Ошибка сервера";
        errorDiv.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("mode") === "register") {
        showRegister();
    } else {
        showLogin();
    }

    const regForm = document.getElementById("register-form");
    if (regForm) {
        regForm.onsubmit = handleRegister;
    }
});