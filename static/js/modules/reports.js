document.addEventListener('DOMContentLoaded', function() {
    // Функция для генерации HTML строки таблицы
    function createReportRow(report, index) {
        return `
            <th scope="row">${index}</th>
            <td>${report.name || '-'}</td>
            <td>${report.organization?.name || '-'}</td>
            <td>${report.user?.first_name || '-'}</td>
            <td>${report.created_date ? new Date(report.created_date).toLocaleString() : '-'}</td>
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

    async function filterStatus0Reports(reports) {
        const filteredReports = []

        Object.keys(reports).forEach(reportKey => {
            if (reports[reportKey].status !== 4) {
                filteredReports.push(reports[reportKey])
            }
        })

        return filteredReports

    }

    async function loadReports() {
        try {
            let url = `${window.location.origin}/${window.location.pathname.split('/')[1]}/reports/reports_list/`;

            const response = await fetch(url, {
                credentials: 'include',      // Для аутентификации
                cache: 'no-store',          // Отключает кэширование
            });
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
            if (!document.querySelector('.reports-block-inner-table .reports-text-none')) {
                const noReportsDiv = document.createElement('div');
                noReportsDiv.className = 'reports-text-none';
                noReportsDiv.textContent = 'У вас нет уведомлений';
                document.getElementById('reportsContainer').appendChild(noReportsDiv);
                document.getElementById('reportsTable').style.display = 'none';
            }
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
                    index++;
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

    let reports;   // объявили переменную reports

    (async () => {
        await loadReports();
        const reportsString = localStorage.getItem('reports');
        if (reportsString) {
            reports = JSON.parse(reportsString);
            await fillTable(reports);
        }
    })();

    const sortBtn = document.getElementById('sort-btn');
    if (sortBtn) {
        sortBtn.addEventListener('click', async () => {
            if (reports) {
                await fillTable(reports, 'DONE');
            }
        });
    }
    const filterBtn = document.getElementById('zeroReports-btn');
    let filteredReports;
    if (filterBtn) {
        filterBtn.addEventListener('click', async () => {
            if (reports) {
                filteredReports = await filterStatus0Reports(reports)
                await fillTable(filteredReports);
            }
        });
    };

    const downloadZipBtn = document.getElementById('download-btn')
    console.log(downloadZipBtn);
    if (downloadZipBtn) {
        downloadZipBtn.addEventListener('click', async () => {
            filteredReports = await filterStatus0Reports(reports)
            if (filteredReports.length > 0) {
                console.log('добавляем обработчик для кнопки');
                const notDownladedReportsID = []
                Object.keys(filteredReports).forEach(reportKey => {
                    if (filteredReports[reportKey].status !== 4) {
                        notDownladedReportsID.push(filteredReports[reportKey].id)
                    }
                });
                console.log(notDownladedReportsID);
                const downloadUrl = `${window.location.origin}/${window.location.pathname.split('/')[1]}/reports/download-zip/`
                if (notDownladedReportsID.length > 0) {
                    const response = await fetch(downloadUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(notDownladedReportsID)
                    });

                    if (!response.ok) {
                        throw new Error(`не удалось скачать файл`);
                    }

                    // Получаем zip-файл как Blob
                    const blob = await response.blob();

                    // Создаём временную ссылку для скачивания
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'archive.zip'; // имя файла
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    console.log('Скачали файл')
                }
            }
        })
    }
});