// static/js/deals.js
document.addEventListener("DOMContentLoaded", () => {
    const editForm = document.getElementById("edit-form");
    const selectedIdInput = document.getElementById("selected-id");

    document.querySelectorAll(".deal-row").forEach(row => {
        row.addEventListener("click", () => {
            // Подсветка выбранной строки
            document.querySelectorAll(".deal-row").forEach(r => r.classList.remove("selected"));
            row.classList.add("selected");

            const id = row.dataset.id;
            selectedIdInput.value = id;
            
            // Автозаполнение полей редактирования из data-атрибутов
            document.getElementById("edit-asset").value = row.dataset.asset;
            document.getElementById("edit-direction").value = row.dataset.direction;
            document.getElementById("edit-amount").value = row.dataset.amount;
            document.getElementById("edit-entry").value = row.dataset.entry;
            document.getElementById("edit-exit").value = row.dataset.exit;
            document.getElementById("edit-tf").value = row.dataset.tf;
            document.getElementById("edit-comment").value = row.dataset.comment;
            document.getElementById("edit-date").value = row.dataset.date;

            // замена URL формы
            editForm.action = "/deals/update/" + id;
        });
    });
});