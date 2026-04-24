// static/js/profile.js

// 1. Валидация смены пароля
const passwordForm = document.getElementById("password-form");
if (passwordForm) {
    passwordForm.addEventListener("submit", function(e) {
        const newPass = document.getElementById("new-pass").value.trim();
        const confirm = document.getElementById("confirm-pass").value.trim();

        if (newPass.length < 6) {
            alert("Пароль слишком короткий (минимум 6 символов)!");
            e.preventDefault();
            return;
        }
        if (newPass !== confirm) {
            alert("Пароли не совпадают!");
            e.preventDefault();
        }
    });
}

// 2. График динамики портфеля
const ctxProfile = document.getElementById("chart");
if (ctxProfile && window.profileChartData) {
    new Chart(ctxProfile, {
        type: "line",
        data: {
            labels: window.profileChartData.map(d => d.date),
            datasets: [{
                label: "Баланс",
                data: window.profileChartData.map(d => d.balance),
                borderColor: "#7b2ff7",
                backgroundColor: "rgba(123, 47, 247, 0.1)",
                borderWidth: 3,
                pointRadius: 5,
                pointBackgroundColor: "#7b2ff7",
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: "#777" }, grid: { display: false } },
                y: { ticks: { color: "#777" }, grid: { color: "#222" } }
            }
        }
    });
}