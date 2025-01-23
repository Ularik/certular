//<!--REGISTRATION-->


const regForm = document.querySelector('.registration__form');
const regFormBlocks = regForm.querySelectorAll('.registration__form-block');
const regFormBtn = document.querySelector('.registration__form-btn');
const csrftokenWriteReg = document.getElementsByName('csrfmiddlewaretoken');
let urlReg = `${window.location.origin}/${window.location.pathname.split('/')[1]}/accounts/registration/`;
let urlRegSuccess = `${window.location.origin}/${window.location.pathname.split('/')[1]}/accounts/check/registration/`;

const regObj = {
    organization: '',
    first_name: '',
    last_name: '',
    patronymic: '',
    position: '',
    date_of_birth: '',
    email: '',
    number: '',
    csrfmiddlewaretoken: '',
};
let demoForm = document.getElementById('captcha-from')

let regexRegEmail = new RegExp("^[A-Za-z0-9_!#$%&'*+\\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$");
let regexName = new RegExp("^[ёЁa-zA-ZА-Яа-я ]+$");
let regexDate = new RegExp("^[0-9.]{8,}?$");
let regexTel = new RegExp("^[0-9+ ]{12,}?$");
let regexRegSelect = new RegExp("^[0-9]{1,}?$");

const validateToolTipReg = (elem, className) => {
    const errorValid = document.querySelector(`#errorValid-${className}`);

    regFormBlocks.forEach(a => {
        a.style.position = 'relative';
        if (a.contains(elem) && !a.contains(errorValid)) {
            let lang = window.location.pathname;
            if (lang.includes('ru')) {
                let valueError =
                    `
                    <p class="errorValid" id="errorValid-${className}">Пожалуйста, заполните это поле</p>
                `;
                a.insertAdjacentHTML("beforeend", valueError);
            } else if (lang.includes('ky')) {
                let valueError =
                    `
                    <p class="errorValid" id="errorValid-${className}">Сураныч, бул талааны толтуруңуз</p>
                `;
                a.insertAdjacentHTML("beforeend", valueError);
            } else if (lang.includes('en')) {
                let valueError =
                    `
                    <p class="errorValid" id="errorValid-${className}">Please fill out this field</p>
                `;
                a.insertAdjacentHTML("beforeend", valueError);
            }

            setTimeout(() => {
                document.querySelectorAll('.errorValid').forEach(error => {
                    error.remove();
                })
            }, 5000);
        }
    })
}

const regexValidReg = (regex, className, value, elem, domElem) => {
    const errorValid = document.querySelector(`#errorValid-${className}`);
    if (regex.test(value)) {
        if (errorValid) {
            errorValid.remove();
        }
        value = elem;

    } else {
        value = '';
        validateToolTipReg(domElem, className);

    }
}

regFormBtn.addEventListener('click', () => {
    regexValidReg(regexName, `last_name`, regObj.last_name, regForm.elements.last_name.value, regForm.elements.last_name);
    regexValidReg(regexName, `first_name`, regObj.first_name, regForm.elements.first_name.value, regForm.elements.first_name);
    regexValidReg(regexName, `patronymic`, regObj.patronymic, regForm.elements.patronymic.value, regForm.elements.patronymic);
    regexValidReg(regexDate, `date_of_birth`, regObj.date_of_birth, regForm.elements.date_of_birth.value, regForm.elements.date_of_birth);
    regexValidReg(regexRegEmail, `reg-email`, regObj.email, regForm.elements.email.value, regForm.elements.email);
    regexValidReg(regexTel, `number`, regObj.number, regForm.elements.number.value, regForm.elements.number);
    regexValidReg(regexRegSelect, `organization`, regObj.organization, regForm.elements.organization.value, regForm.elements.organization);
});


regForm.addEventListener('change', (e) => {
    // e.preventDefault();

    regObj.organization = regForm.elements.organization.value;
    regObj.first_name = regForm.elements.first_name.value;
    regObj.last_name = regForm.elements.last_name.value;
    regObj.patronymic = regForm.elements.patronymic.value;
    regObj.date_of_birth = regForm.elements.date_of_birth.value;
    regObj.email = regForm.elements.email.value;
    regObj.number = regForm.elements.number.value;
    regObj.csrfmiddlewaretoken = csrftokenWriteReg[0].value;

    regObj.date_of_birth = regObj.date_of_birth.split('-').join('.');
    const yearBirth = regObj.date_of_birth.slice(0, 4);
    const monthsBirth = regObj.date_of_birth.slice(4, 7);
    const dayBirth = regObj.date_of_birth.slice(8, 10);
    regObj.date_of_birth = dayBirth + monthsBirth + '.' + yearBirth;

    regObj.number = regObj.number.split(' ').join('');
    regObj.number = regObj.number.split(')').join('');
    regObj.number = regObj.number.split('(').join('');
    regObj.number = regObj.number.split('+').join('');
})

function onSubmitReg(token) {
    console.log(regObj);

    if (regObj.number.length === 12 && regObj.organization) {
        fetch(urlReg, {
            method: 'POST',
            body: {'hello': 'world'},

        }).then(res => {
            return res.json()
        }).then(res => {
            if (res?.success) {
                window.location.replace(`${urlRegSuccess}`);
            } else if (res?.error) {
                const el = document.getElementById('errorMsgReg');
                el.innerText = res.error.toString();
            }
        })
    }

}


//<!--SEND MESSAGE-->

const selectDefault = ['file', 'ip', 'domain', 'hash'];
const selectChangeable = [];

const reportObj = {
    email: '',
    full_name: '',
    description: '',
    phone_number: '',
    host_ip: '',
    domain_name: '',
    hash: '',
    file: '',
    csrfmiddlewaretoken: '',
    all2send: false,
};

let indicators = [];
let countReport = 'count-1';

const reportBackdropForm = document.querySelector('#reportBackdrop .report_form');
const reportBackdropFormBlocks = reportBackdropForm.querySelectorAll('.report__form-block');
const reportBtnAdd = document.querySelector('#reportBackdrop .indicators-btn .indicators-add-btn');
const reportindicatorsBox = document.querySelector('#reportBackdrop .indicators-block-boxes');
let allIndicators = document.querySelectorAll('#reportBackdrop .indicators-box')
const csrftokenReport = document.getElementsByName('csrfmiddlewaretoken');
let urlReportBackdropForm = `${window.location.origin}/${window.location.pathname.split('/')[1]}/messages/send/`;

if (reportBackdropForm) {
    const firstIndicator = document.querySelector('#reportBackdrop .indicators-box');
    reportBtnAdd.style.display = "none";

    firstIndicator.addEventListener('click', e => {
        const value = e.target.value
        let input = firstIndicator.querySelector('.indicators-file>input')
        let select = firstIndicator.querySelector('.form-control.report-select')

        if (selectDefault.includes(value)) {
            input.addEventListener('keyup', e => {
                e.preventDefault()

                if (e.target.value === '' || e.target.value === null || e.target.value === undefined) {
                    select.disabled = false;
                    reportBtnAdd.style.display = "none";
                } else if (e.target.value !== '') {
                    select.disabled = true;
                    reportBtnAdd.style.display = "block";
                }
            })
            input.addEventListener('change', e => {
                if (e.target.value !== '') {
                    select.disabled = true;
                    reportBtnAdd.style.display = "block";
                } else if (e.target.value === '' || e.target.value === null || e.target.value === undefined) {
                    select.disabled = false;
                }
            })

            input.type = value === 'file' ? 'file' : 'text';
            input.id = `${value}`;
            input.name = `${value}`;

            if (selectChangeable.length) {
                selectChangeable.pop();
            }

            selectChangeable.push(value);
            input.disabled = false;
        }
    })

    reportBtnAdd.addEventListener('click', async (e) => {
        e.preventDefault()

        let divBlock = `
                    <div class="indicators-box">
                        <div class="indicators-block">
                            <div class="indicators-type">
                                <select name="indicators-type-select"
                                        class="form-control report-select ${countReport + 1}"
                                        aria-label="Default select example"
                                >
                                    <option selected disabled hidden value="">
                                        Индикатор
                                    </option>
                                </select>
                                <svg class="indicators-type-svg" width="10" height="5" viewBox="0 0 10 5" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4.45652 5L-2.0465e-07 -4.37114e-07L1.73913 -3.61094e-07L4.97283 3.8354L4.86413 3.80435L5.13587 3.80435L5.02717 3.8354L8.26087 -7.60198e-08L10 0L5.54348 5L4.45652 5Z" fill="#003467"/>
                                </svg>
                            </div>
                            <div class="indicators-file">
                                <input type="text"
                                       class="form-control"
                                       id="other"
                                       name="other"
                                       disabled
                                >
                            </div>
                            <button class="report-btn-delete">
                            <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="1.84884" height="18.4884" rx="0.924418" transform="matrix(0.681189 0.732107 -0.681189 0.732107 12.7578 0.111328)" fill="#EF2E22"/>
                                <rect width="1.84884" height="18.4884" rx="0.924418" transform="matrix(0.681189 -0.732107 0.681189 0.732107 0.164062 1.46484)" fill="#EF2E22"/>
                            </svg>
                            </button>
                        </div>
                    </div>
          `
        reportindicatorsBox.insertAdjacentHTML("beforeend", divBlock);
        countReport += 1

        const addOptions = () => {
            const reportIndicatorsSelect = document.querySelector(`.report_form select.form-control.${countReport}`);
            let allIndicators = document.querySelectorAll('#reportBackdrop .indicators-box')

            allIndicators.forEach(boxIndicators => {
                const btnDelete = boxIndicators.querySelector('.report-btn-delete');
                const select = boxIndicators.querySelector('.form-control.report-select');
                const input = boxIndicators.querySelector(`.indicators-file>input`);

                if (btnDelete) {
                    btnDelete.addEventListener('click', async () => {
                        await boxIndicators.remove();

                        if (selectChangeable.length + 1 !== allIndicators.length) {
                            await selectChangeable.pop();
                        }

                        allIndicators = document.querySelectorAll('#reportBackdrop .indicators-box')
                        const lastInputBox = allIndicators[allIndicators.length - 1].querySelector('.indicators-file>input');
                        if (lastInputBox !== '') {
                            reportBtnAdd.style.display = "block";
                        } else if (lastInputBox === '') {
                            reportBtnAdd.style.display = "none";
                        }
                    })
                }

                boxIndicators.addEventListener('click', e => {
                    const value = e.target.value

                    if (selectDefault.includes(value)) {
                        input.addEventListener('keyup', e => {
                            if (e.target.value === '' || e.target.value === null || e.target.value === undefined) {
                                // select.disabled = false;
                                reportBtnAdd.style.display = "none";
                            } else if (e.target.value !== '') {
                                select.disabled = true;
                                if (allIndicators.length >= 4) {
                                    reportBtnAdd.style.display = "none";
                                } else if (allIndicators.length !== 4) {
                                    reportBtnAdd.style.display = "block";
                                }
                            }
                        })
                        input.addEventListener('change', e => {
                            if (e.target.value !== '') {
                                select.disabled = true;
                                if (allIndicators.length >= 4) {
                                    reportBtnAdd.style.display = "none";
                                } else if (allIndicators.length !== 4) {
                                    reportBtnAdd.style.display = "block";
                                }
                            } else if (e.target.value === '' || e.target.value === null || e.target.value === undefined) {
                                select.disabled = false;
                                reportBtnAdd.style.display = "none";
                            }
                        })
                        input.type = value === 'file' ? 'file' : 'text';
                        input.id = `${value}`;
                        input.name = `${value}`;

                        if (!selectChangeable.includes(value)) {
                            selectChangeable.push(value)
                            select.disabled = true
                        }

                        input.disabled = false;

                        if (allIndicators.length >= 4) {
                            reportBtnAdd.style.display = "none";
                        }
                    }
                })

            })

            selectDefault.filter(elem => !selectChangeable.includes(elem)).map(a => {
                let option =
                    `
                    <option value="${a}">${a}</option>
                `
                reportIndicatorsSelect.insertAdjacentHTML("beforeend", option);
            })
        }

        await addOptions();
        if (selectChangeable.length >= 4) {
            reportBtnAdd.style.display = "none";
        }
        reportBtnAdd.style.display = "none";

    })

    const btnSubmit = reportBackdropForm.querySelector('button.main-btn');

    let regexReportEmail = new RegExp("^[A-Za-z0-9_!#$%&'*+\\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$");
    let regexReportFullName = new RegExp("^[ёЁa-zA-ZА-Яа-я ]+$");
    let regexReportTel = new RegExp("^[0-9+() ]{18,}?$");
    let regexReportMessage = new RegExp("^[a-zA-Z0-9А-Яа-я- ёЁ]{2,10000}?$");

    const validateToolTipReport = (elem, className) => {
        const errorValid = document.querySelector(`#errorValid-${className}`);

        reportBackdropFormBlocks.forEach(a => {
            a.style.position = 'relative';
            if (a.contains(elem) && !a.contains(errorValid)) {
                let lang = window.location.pathname;
                if (lang.includes('ru')) {
                    let valueError =
                        `
                    <p class="errorValid" id="errorValid-${className}">Пожалуйста, заполните это поле</p>
                `;
                    a.insertAdjacentHTML("beforeend", valueError);
                } else if (lang.includes('ky')) {
                    let valueError =
                        `
                    <p class="errorValid" id="errorValid-${className}">Сураныч, бул талааны толтуруңуз</p>
                `;
                    a.insertAdjacentHTML("beforeend", valueError);
                } else if (lang.includes('en')) {
                    let valueError =
                        `
                    <p class="errorValid" id="errorValid-${className}">Please fill out this field</p>
                `;
                    a.insertAdjacentHTML("beforeend", valueError);
                }

                setTimeout(() => {
                    document.querySelectorAll('.errorValid').forEach(error => {
                        error.remove();
                    })
                }, 5000);
            }

        })


    }

    const regexValidReport = (regex, className, value, elem, domElem) => {
        const errorValid = document.querySelector(`#errorValid-${className}`);
        if (regex.test(value)) {
            if (errorValid) {
                errorValid.remove();
            }
            value = elem;

        } else {
            value = '';
            validateToolTipReport(domElem, className);

        }
    }

    btnSubmit.addEventListener('click', () => {
        regexValidReport(regexReportEmail, `reg-email`, reportObj.email, reportBackdropForm.elements.email.value, reportBackdropForm.elements.email);
        regexValidReport(regexReportFullName, `full_name`, reportObj.full_name, reportBackdropForm.elements.full_name.value, reportBackdropForm.elements.full_name);
        regexValidReport(regexReportTel, `phone_number`, reportObj.phone_number, reportBackdropForm.elements.phone_number.value, reportBackdropForm.elements.phone_number);
        regexValidReport(regexReportMessage, `description`, reportObj.description, reportBackdropForm.elements.description.value, reportBackdropForm.elements.description);
    })

    reportBackdropForm.addEventListener('change', e => {
        // e.preventDefault()

        reportObj.email = reportBackdropForm.elements.email.value;
        reportObj.full_name = reportBackdropForm.elements.full_name.value;
        reportObj.description = reportBackdropForm.elements.description.value;
        reportObj.phone_number = reportBackdropForm.elements.phone_number.value;
        reportObj.host_ip = reportBackdropForm.elements.ip?.value || '';
        reportObj.domain_name = reportBackdropForm.elements.domain?.value || '';
        reportObj.hash = reportBackdropForm.elements.hash?.value || '';
        reportObj.file = reportBackdropForm.elements.file?.files[0] || '';
        reportObj.csrfmiddlewaretoken = csrftokenReport[0].value;
        reportObj.all2send = !!reportBackdropForm.elements.all2send?.checked
    })

    function onSubmitMessage() {
        console.log(reportObj);
        const formData = new FormData();
        const formObj = {};

        Object.keys(reportObj).forEach(key => {
            formObj[key] = reportObj[key];
        });

        console.log(formObj);
        if (reportObj.phone_number.length === 18) {
            fetch(urlReportBackdropForm, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftokenReport[0].value
                },
                body: formObj,
            }).then(async res => {
                if (res.status === 200) {
                    await $('#reportBackdrop').modal('hide');
                    await new bootstrap.Modal(document.getElementById('modalContact')).show();

                    reportBackdropForm.elements.phone_number.value = ''
                    reportBackdropForm.elements.description.value = ''

                    reportObj.phone_number = '';
                    reportObj.description = '';
                }
                if (res.status !== 200) return res.json()
            }).then(res => {
                if (res?.error) {
                    const el = document.getElementById('errorReportModal');
                    el.innerText = res.error.toString();
                }
            })
        }

    }
}
