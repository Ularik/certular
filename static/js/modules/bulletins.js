async function get_bulletins() {
    const url = `${window.location.origin}/${window.location.pathname.split('/')[1]}/bulletins/get_list/`;
    const response = await fetch(url)
    const bulletines = await response.json()
    return bulletines
};

function sortBulletineOnWeeks(bulletines) {
    let firstBulletineDate = new Date(bulletines[0].created_at);

    let startWeeksDate = getCurrentMonday(firstBulletineDate) // первый понедельник
    const oneDayMs = 24 * 60 * 60 * 1000;
    let endWeekMs = startWeeksDate.getTime() + oneDayMs * 7;  // конец недели в секундах

    let endWeeksDate = new Date(endWeekMs);

    let dateTitle = `${getDateString(startWeeksDate)} - ${getDateString(endWeeksDate)}`;
    const weeks = {}

    bulletines.forEach((bulletine) => {
        const date = new Date(bulletine.created_at);

        if (endWeeksDate.getTime() > date.getTime() && date.getTime() > startWeeksDate.getTime()) {
            if (!weeks[dateTitle]) {
                weeks[dateTitle] = [];
            }

            weeks[dateTitle].push(bulletine);
        } else {
            startWeeksDate = date; //переопределяем начало недели

            startWeeksMs = startWeeksDate.getTime()
            endWeeksDate = new Date(startWeekMs + oneDayMs * 7);

            dateTitle = getDateString(startWeeksDate) - getDateString(endWeeksDate);

            weeks[dateTitle] = [bulletine]
        }

    });
    return weeks;
}

function getDateString(date) {
    const day = String(date.getDate()).padStart(2, '0'); // День с ведущим нулем
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяц (нумерация с 0, поэтому +1)
    const year = String(date.getFullYear()).slice(-2); // Последние две цифры года

    const formattedDate = `${day}.${month}.${year}`;
    return formattedDate;
};

function getCurrentMonday(date = new Date()) {
    const day = date.getDay(); // 0 (вс) - 6 (сб)
    const diff = (day === 0 ? -6 : 1 - day); // если воскресенье — отнимаем 6, иначе ищем понедельник
    const monday = new Date(date);
    monday.setDate(date.getDate() + diff);
    monday.setHours(0, 0, 0, 0); // обнуляем время
    return monday;
}

function addBulletin(bulletinesWeekBlock, titleText, bodyText) {
    const list = bulletinesWeekBlock.querySelector('.bulletines-list');
    const template = bulletinesWeekBlock.querySelector('.bulletines-item');
    template.style.display = "none";

    const clone = template.cloneNode(true);
    clone.style.display = 'block';
    const titleLink = clone.querySelector('.bulletines-open-link')
    const bulletineBody = clone.querySelector('.bulletines-body')

    // Изменяем содержимое
    titleLink.lastChild.textContent = titleText;
    bulletineBody.innerHTML  = bodyText;

    list.appendChild(clone);

    titleLink.addEventListener('click', (event) => {
        event.preventDefault();
        showBulletineBody(bulletineBody);
    });
};


function showBulletineBody(bulletineBody) {

    if (getComputedStyle(bulletineBody).display === 'none') {
        bulletineBody.style.display = 'block';
    } else {
        bulletineBody.style.display = 'none';
    }
};


async function fillPageBilletines() {
    const bulletines = await get_bulletins();

    const weeksOfBulletines = sortBulletineOnWeeks(bulletines)

    Object.keys(weeksOfBulletines).forEach(weekName => {

        const bulletinesDateBlock = document.querySelector('.bulletines-week-block');
        const clone = bulletinesDateBlock.cloneNode(true);
        bulletinesDateBlock.style.display = 'none'

        const cloneDateTitle = clone.querySelector('.bulletines-week-time');
        cloneDateTitle.textContent = weekName;

        const oneWeekBulletines = weeksOfBulletines[weekName];

        oneWeekBulletines.forEach(bulletine => {
            addBulletin(clone, bulletine.title, bulletine.description);
        });
        document.querySelector('.bulletines-block').appendChild(clone);
    });
};

fillPageBilletines();
