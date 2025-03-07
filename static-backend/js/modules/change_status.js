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
        const selectTag = event.target;
        const optionsList = selectTag.querySelectorAll('option')
        console.log(selectTag)
        if (data.status === 4) {
            console.log(data.status);
            selectTag.value = optionsList[0].value
        } else {
            console.log(data.status);
            selectTag.value = optionsList[1].value
        }
        localStorage.setItem(`report-status-${reportId}`, event.target.value); // Сохраняем выбор
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

for (const statusBtn of statusBtns) {

    const optionTag = document.createElement('option')
    const option2Tag = document.createElement('option')
    optionTag.classList.add('status-btn')
    option2Tag.classList.add('status-btn')

    let lang = window.location.pathname;

    let text1 = 'Выполненно'
    let text2 = 'Не выполненно'

    if (lang.includes('ky')) {
        text1 = 'Аткарылды'
        text2 = 'Аткарылбады'
    } else if (lang.includes('en')) {
        text1 = 'had done'
        text2 = 'had not done'
    }
    optionTag.innerText = text1
    option2Tag.innerText = text2

    statusBtn.appendChild(optionTag)
    statusBtn.appendChild(option2Tag)

    const reportId = statusBtn.getAttribute('data-report-id');
    const savedValue = localStorage.getItem(`report-status-${reportId}`);

    if (savedValue !== null) {
        statusBtn.value = savedValue
    } else {
        statusBtn.value = parseInt(statusBtn.getAttribute('data-report-status'), 10) === 4
            ? optionTag.value
            : option2Tag.value;
        console.log(statusBtn.value)
    }

    statusBtn.addEventListener('change', (event) => changeReportStatus(event));
};

