// static/js/analytics.js

const purple = "#7b2ff7";
const gridColor = "rgba(255, 255, 255, 0.05)";
const textColor = "#777";

Chart.defaults.color = textColor;
Chart.defaults.font.family = "'Segoe UI', sans-serif";

// 1. График капитала
const ctxProfit = document.getElementById("profitChart");
if (ctxProfit && window.chartData) {
    new Chart(ctxProfit, {
        type: "line",
        data: {
            labels: window.chartData.map(d => d.date),
            datasets: [{
                label: "Баланс",
                data: window.chartData.map(d => d.balance),
                borderColor: purple,
                backgroundColor: "rgba(123, 47, 247, 0.1)",
                borderWidth: 3,
                pointRadius: 5,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: "#222" } }
            }
        }
    });
}

// 2. Круговой график активов
const ctxAssets = document.getElementById("assetsChart");
if (ctxAssets && window.assetsData) {
    new Chart(ctxAssets, {
        type: "doughnut",
        data: {
            labels: Object.keys(window.assetsData),
            datasets: [{
                data: Object.values(window.assetsData),
                backgroundColor: ["#7b2ff7", "#9b00ff", "#5a1fd7", "#3b0ca3", "#1a1a1a"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: '#aaa' } } },
            cutout: '70%'
        }
    });
}

// 3. Сделки по дням
const ctxWeek = document.getElementById("weekChart");
if (ctxWeek && window.weekData) {
    const orderedDays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
    const orderedValues = orderedDays.map(day => window.weekData[day] || 0);

    new Chart(ctxWeek, {
        type: "bar",
        data: {
            labels: orderedDays,
            datasets: [{
                data: orderedValues,
                backgroundColor: purple,
                borderRadius: 8,
                barThickness: 40
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: true, grid: { color: gridColor }, ticks: { stepSize: 1 } }
            }
        }
    });
}