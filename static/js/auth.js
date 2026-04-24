// static/js/auth.js
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

function validateRegister() {
    const pass = document.getElementById("reg-password").value;
    const confirm = document.getElementById("reg-confirm").value;
    const balance = document.getElementById("start-balance").value;

    if (pass.length < 6) {
        alert("Пароль должен быть минимум 6 символов");
        return false;
    }
    if (pass !== confirm) {
        alert("Пароли не совпадают");
        return false;
    }
    if (!balance || balance <= 0) {
        alert("Начальный баланс должен быть больше 0");
        return false;
    }
    return true;
}

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("mode") === "register") {
        showRegister();
    } else {
        showLogin();
    }
});