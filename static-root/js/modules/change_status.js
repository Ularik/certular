const statusBtns = document.querySelectorAll("select.status-btn")

const statusList = document.querySelectorAll("option.status-btn")

function changeReportStatus(event) {
    event.preventDefault(); // Отключаем стандартное действие по клику

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Получаем CSRF токен
    console.log(event.target)
    const reportId = event.target.getAttribute('data-report-id');
    const url = event.target.getAttribute('data-url');
    console.log(event.target.value)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Добавляем CSRF-токен
        },
        body: JSON.stringify({
            status: event.target.value, // Укажите новое значение статуса
        }),
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Предполагаем, что сервер вернёт JSON
        } else {
            throw new Error('Не удалось изменить статус');
        }
    })
    .then(data => {
        // Обновляем текст ссылки или выполняем другие действия
        const option = event.target;
        if (data.status === 4) {
            console.log(data.status);
        } else {
            console.log(data.status);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

for (const statusBtn of statusBtns) {
    statusBtn.addEventListener('change', (event) => changeReportStatus(event));
};

