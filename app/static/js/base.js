document.addEventListener("DOMContentLoaded", function() {
    // Получаем элемент кружка с числом уведомлений
    var notificationCountElement = document.getElementById("notificationCount");

    // Проверяем, есть ли уведомления (если переменная notifications_num не пуста)
    if (!notificationCountElement.innerText.trim()) {
        // Скрываем элемент, если уведомлений нет
        notificationCountElement.style.display = "none";
    }
});