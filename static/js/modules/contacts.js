document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('appeals-form');
    const errorContainer = document.getElementById('errorMsgContacts');
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const apiUrl = form.getAttribute("action");

    // Функция для получения токена
    const getRecaptchaToken = () => {
        return new Promise((resolve, reject) => {
            if (typeof grecaptcha === 'undefined') {
                reject(new Error('reCAPTCHA не загружен'));
                return;
            }
            grecaptcha.ready(() => {
                grecaptcha.execute('6LfXqfYqAAAAANmQu7Ewp2AgVO8mPTj5XIIO2NFU', { action: 'submit' })
                    .then(token => resolve(token))
                    .catch(error => reject(error));
            });
        });
    };

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorContainer.textContent = '';

        const formData = {
            email: form.email.value,
            token: '',
            full_name: form.full_name.value,
            phone_number: form.phone_number.value,
            organization: form.organization.value,
            message: form.message.value,
        };

        try {
            const token = await getRecaptchaToken();
            formData.token = token;

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                alert('Сообщение отправлено успешно!');
                form.reset();
            } else {
                const data = await response.json();
                errorContainer.textContent = data.errors?.toString() || 'Ошибка при отправке формы.';
            }
        } catch (error) {
            console.error('Ошибка:', error);
            errorContainer.textContent = error.message || 'Ошибка сети. Попробуйте позже.';
        }
    });
});