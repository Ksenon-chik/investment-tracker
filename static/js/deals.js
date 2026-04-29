document.addEventListener("DOMContentLoaded", () => {
    const editForm = document.getElementById("edit-form");
    const deleteForm = document.querySelector('form[action="/deals/delete-selected"]');
    const selectedIdInput = document.getElementById("selected-id");
    const notificationContainer = document.getElementById("notification-container");

    // Функция для показа уведомлений
    function showToast(message, type = 'error') {
        const toast = document.createElement("div");
        toast.className = `notification ${type}`;
        toast.innerText = message;
        notificationContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    selectedIdInput.value = ""; 

    document.querySelectorAll(".deal-row").forEach(row => {
        row.addEventListener("click", () => {
            document.querySelectorAll(".deal-row").forEach(r => r.classList.remove("selected"));
            row.classList.add("selected");

            const id = row.dataset.id;
            selectedIdInput.value = id;
            
            // Заполнение полей
            document.getElementById("edit-asset").value = row.dataset.asset;
            document.getElementById("edit-direction").value = row.dataset.direction;
            document.getElementById("edit-amount").value = row.dataset.amount;
            document.getElementById("edit-entry").value = row.dataset.entry;
            document.getElementById("edit-exit").value = row.dataset.exit;
            document.getElementById("edit-tf").value = row.dataset.tf;
            document.getElementById("edit-comment").value = row.dataset.comment;
            document.getElementById("edit-date").value = row.dataset.date;

            editForm.action = "/deals/update/" + id;
        });
    });

    // Валидация редактирования
    editForm.addEventListener('submit', (event) => {
        if (!selectedIdInput.value) {
            event.preventDefault();
            showToast('Сначала выберите сделку в таблице');
        }
    });

    // предупреждение перед удалением
    deleteForm.addEventListener('submit', (event) => {
        if (!selectedIdInput.value) {
            event.preventDefault();
            showToast('Выберите сделку для удаления');
        } else {
            const confirmDelete = confirm("Вы уверены, что хотите удалить эту сделку? Это действие нельзя отменить.");
            if (!confirmDelete) {
                event.preventDefault();
            }
        }
    });
});