document.addEventListener('DOMContentLoaded', function() {
    // Функция для генерации HTML строки таблицы
    function createReportRow(report, index) {
        return `
            <th scope="row">${index + 1}</th>
            <td>${report.name || '-'}</td>
            <td>${report.organization?.name || '-'}</td>
            <td>${report.user?.username || '-'}</td>
            <td>${report.created_date || '-'}</td>
            ${report.file ?
                `<td class="reports-btn-td">
                    <a class="main-btn reports-download"
                       href="/reports/download/${report.id}/"
                       download>Скачать файл</a>
                </td>` :
                '<td>-</td>'
            }
            <td class="reports-btn-td">
                <select class="status-btn"
                        data-report-id="${report.id}"
                        data-report-status="${report.status}"
                        data-url="/reports/change/${report.id}/">
                </select>
            </td>`;
    }

    // Функция для настройки select элементов
    function setupStatusButtons(statusBtns) {
        const lang = window.location.pathname;
        let text1 = 'Выполнено';
        let text2 = 'Не выполнено';
        if (lang.includes('ky')) {
            text1 = 'Аткарылды';
            text2 = 'Аткарылбады';
        } else if (lang.includes('en')) {
            text1 = 'Done';
            text2 = 'Not Done';
        }

        statusBtns.forEach(statusBtn => {
            const optionTag = document.createElement('option');
            const option2Tag = document.createElement('option');
            optionTag.innerText = text1;
            option2Tag.innerText = text2;
            optionTag.value = '4';
            option2Tag.value = '0';

            statusBtn.appendChild(optionTag);
            statusBtn.appendChild(option2Tag);

            const reportId = statusBtn.getAttribute('data-report-id');
            const reports = JSON.parse(localStorage.getItem('reports') || '{}');
            const savedValue = (parseInt(reports[reportId].status, 10) === 4 ? '4' : '0');
            statusBtn.value = savedValue !== null ? savedValue : (parseInt(statusBtn.getAttribute('data-report-status'), 10) === 4 ? '4' : '0');

            statusBtn.addEventListener('change', changeReportStatus);
        });
    }

    async function loadReports() {
        try {
            let url = `${window.location.origin}/${window.location.pathname.split('/')[1]}/reports/reports_list/`;

            const response = await fetch(url);
            if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
            const reports = await response.json();
            const data = {}
            reports.forEach((report) => {
                data[report.id] = report
            });
            localStorage.setItem(`reports`, JSON.stringify(data));

        } catch (error) {
            console.error('Ошибка при загрузке отчетов:', error);
        }
    }

    async function changeReportStatus(event) {
        event.preventDefault();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const reportId = event.target.getAttribute('data-report-id');
        const urlChangeStatus = event.target.getAttribute('data-url');

        try {
            const response = await fetch(urlChangeStatus, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    status: event.target.value,
                }),
            });

            if (!response.ok) {
                throw new Error(`Не удалось изменить статус: ${response.status}`);
            }

            const data = await response.json();

            const reportsString = localStorage.getItem(`reports`);
            const reports = JSON.parse(reportsString);
            reports[reportId].status = data.status
            localStorage.setItem(`reports`, JSON.stringify(reports));
        } catch (error) {
            console.error('Ошибка:', error);
        }
    }

    async function fillTable(reports, sort = 'none') {
        const tbody = document.getElementById('reportsBody');
        tbody.innerHTML = '';

        if (Object.keys(reports).length === 0) {
            const noReportsDiv = document.createElement('div');
            noReportsDiv.className = 'reports-text-none';
            noReportsDiv.textContent = 'У вас нет уведомлений';
            document.getElementById('reportsContainer').appendChild(noReportsDiv);
            document.getElementById('reportsTable').style.display = 'none';
            return;
        }

        const filteredReports = []
        let index = 0
        const reportsKeys = Object.keys(reports);
        reportsKeys.forEach((reportKey) => {
            const status = reports[reportKey].status
            if (sort === 'DONE') {
                if (status !== 4) {
                    const row = document.createElement('tr');
                    index++
                    row.innerHTML = createReportRow(reports[reportKey], index);
                    tbody.appendChild(row);
                } else {
                    filteredReports.push(reports[reportKey])
                }
            } else {
                index++
                const row = document.createElement('tr');
                row.innerHTML = createReportRow(reports[reportKey], index);
                tbody.appendChild(row);
            }
        });

        if (filteredReports.length !== 0) {
            filteredReports.forEach((report) => {
                index++
                const row = document.createElement('tr');
                row.innerHTML = createReportRow(report, index);
                tbody.appendChild(row);
            });
            filteredReports.length = 0;
        }

        const statusBtns = document.querySelectorAll("select.status-btn");
        setupStatusButtons(statusBtns);
    }

    (async () => {
        await loadReports();
        const reportsString = localStorage.getItem('reports');
        if (reportsString) {
            const reports = JSON.parse(reportsString);
            await fillTable(reports);
        }
    })();

    const sortBtn = document.querySelector('.sort-btn');
    if (sortBtn) {
        sortBtn.addEventListener('click', async () => {
            const reportsString = localStorage.getItem('reports');
            if (reportsString) {
                const reports = JSON.parse(reportsString);
                await fillTable(reports, 'DONE');
            }
        });
    }
});