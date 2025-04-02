const list_items = {{ data }};
const months = Object.keys(list_items);
const organization_list = {};

const orgDiv = document.querySelector('.organs')

let index = 0
for (const month of months) {
    for (const report of list_items[month]) {

        if (!organization_list[report[1]]) {    # добавляем организацию в список, при отсутствии
            organization_list[report[1]] = {
                allReports: [],
                doneReports: []
            }
        }

        if (organization_list[report[1]].allReports.length !== index + 1) {    # увеличиваем счетчик месяца
            organization_list[report[1]].allReports.push(0)
            organization_list[report[1]].doneReports.push(0)
        }

        organization_list[report[1]].allReports[index] += report[2]    # добавляем все отчеты этой организации
        if (report[0] === 4) {                                         # добавляем только те отчеты, которые выполненны
            organization_list[report[1]].doneReports[index] += report[2]
        }
    }
    index++    # увеличиваем счетчик месяца на 1, в общем с 1 до 6 для графика нужен список отчетов, где каждый эл это один месяц
}

const month_convert = {
    2: 'Январь',
    3: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май'
}

for (const org_name of Object.keys(organization_list)) {
    const btn = document.createElement('button')
    btn.innerText = org_name

    orgDiv.appendChild(btn)

    btn.addEventListener('click', () => changeChart(org_name))
}

let main_org = Object.keys(organization_list)[0]
const chart = organization_list[main_org]
const data1 = chart.allReports
const data2 = chart.doneReports

const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: months,
        datasets: [
            {
                label: 'Отчеты (шт)',
                data: data1,
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.2)',
                fill: true,
                tension: 0.4
            },
            {
                label: 'Выполненные ($K)',
                data: data2,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.2)',
                fill: true,
                tension: 0.4
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function changeChart(org) {
    main_org = org;

    // Обновляем данные графика
    myChart.data.datasets[0].data = organization_list[main_org].allReports;
    myChart.data.datasets[1].data = organization_list[main_org].doneReports;

    myChart.update(); // Перерисовываем график
}
</script>