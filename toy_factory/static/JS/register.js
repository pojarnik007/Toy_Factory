document.addEventListener('DOMContentLoaded', () => {
    const dobInput = document.getElementById('id_date_of_birth');
    const messageBox = document.getElementById('dob-message');
    const submitBtn = document.getElementById('submit-btn');
    const consentBlock = document.getElementById('parent-consent-block');
    const consentCheckbox = document.getElementById('parent-consent-checkbox');

    if (!dobInput) return;


    if (dobInput.getAttribute('type') !== 'date') {
        dobInput.setAttribute('type', 'date');
    }

    const daysOfWeek = [
        'Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'
    ];


    function checkValidity() {
        const inputDate = new Date(dobInput.value);
        const today = new Date();


        if (isNaN(inputDate.getTime())) {
            messageBox.textContent = '';
            dobInput.classList.remove('input-error');
            consentBlock.classList.add('hidden');
            submitBtn.disabled = false;
            return;
        }


        let age = today.getFullYear() - inputDate.getFullYear();
        const monthDiff = today.getMonth() - inputDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < inputDate.getDate())) {
            age--;
        }


        if (age < 18) {

            messageBox.textContent = `Вам ${age} лет. Вы несовершеннолетний.`;
            messageBox.className = 'dob-message error';


            dobInput.classList.add('input-error');


            consentBlock.classList.remove('hidden');


            if (consentCheckbox.checked) {
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
                submitBtn.style.cursor = 'pointer';
            } else {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.5';
                submitBtn.style.cursor = 'not-allowed';
            }

        } else {


            const dayName = daysOfWeek[inputDate.getDay()];


            messageBox.textContent = `Вам ${age} лет. День недели рождения: ${dayName}.`;
            messageBox.className = 'dob-message success';


            dobInput.classList.remove('input-error');
            consentBlock.classList.add('hidden');


            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';

            consentCheckbox.checked = false;
        }
    }


    dobInput.addEventListener('change', checkValidity);
    dobInput.addEventListener('input', checkValidity);
    consentCheckbox.addEventListener('change', checkValidity);
});