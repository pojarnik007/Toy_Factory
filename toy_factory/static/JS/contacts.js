document.addEventListener('DOMContentLoaded', () => {

    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 3000);


    function showLoader() {
        document.body.classList.remove('loaded');
    }

    function hideLoader() {
        document.body.classList.add('loaded');
    }

    function simulateAsyncOperation(callback) {
        showLoader();
        setTimeout(() => {
            try {
                callback();
            } catch (e) {
                console.error("Ошибка при выполнении операции:", e);
                alert("Произошла ошибка (см. консоль F12)");
            } finally {
                hideLoader();
            }
        }, 1000);
    }


    let allData = [];
    let filteredData = [];
    let currentPage = 1;
    const itemsPerPage = 3;
    let sortDirection = 1;
    let currentSortColumn = '';
    let tableBody, paginationDiv, searchInput, searchBtn;
    let addFormBlock, toggleFormBtn, addEmployeeBtn;
    let inputName, inputDesc, inputEmail, inputPhone, inputUrl, validationMsg;
    let detailsBlock, detailsContent, bonusBtn, bonusResult;

    try {
        tableBody = document.getElementById('tableBody');
        paginationDiv = document.getElementById('pagination');
        searchInput = document.getElementById('searchInput');
        searchBtn = document.getElementById('searchBtn');

        addFormBlock = document.getElementById('addFormBlock');
        toggleFormBtn = document.getElementById('toggleFormBtn');
        addEmployeeBtn = document.getElementById('addEmployeeBtn');

        inputName = document.getElementById('addName');
        inputDesc = document.getElementById('addDesc');
        inputEmail = document.getElementById('addEmail');
        inputPhone = document.getElementById('addPhone');
        inputUrl = document.getElementById('addImageUrl');
        validationMsg = document.getElementById('validationMsg');

        detailsBlock = document.getElementById('detailsBlock');
        detailsContent = document.getElementById('detailsContent');
        bonusBtn = document.getElementById('bonusBtn');
        bonusResult = document.getElementById('bonusResult');
    } catch (e) {
        console.error("Ошибка при поиске элементов DOM. Проверьте HTML ID.", e);
    }

    if (!tableBody || !addFormBlock) {
        console.error("Критические элементы не найдены в HTML");
        return;
    }


    if (toggleFormBtn) {
        toggleFormBtn.addEventListener('click', () => {
            addFormBlock.classList.toggle('hidden');
            toggleFormBtn.innerText = addFormBlock.classList.contains('hidden')
                ? 'Добавить сотрудника'
                : 'Скрыть форму';
        });
    }

    fetch('json/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка сети: ${response.status}`);
            }
            return response.json();
        })
        .then(json => {
            console.log("Данные получены:", json);
            allData = json.data;
            filteredData = [...allData];

            setTimeout(() => {
                renderTable();
                renderPagination();
                hideLoader();
            }, 1000);
        })
        .catch(err => {
            console.error('Ошибка fetch:', err);
            hideLoader();
            tableBody.innerHTML = `<tr><td colspan="6" style="color:red; text-align:center;">Ошибка загрузки данных: ${err.message}</td></tr>`;
        });


    function renderTable() {
        tableBody.innerHTML = '';
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const pageData = filteredData.slice(start, end);

        if (pageData.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Нет данных</td></tr>';
            return;
        }

        pageData.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="checkbox" class="select-row" value="${item.name}"></td>
                <td>${item.name}</td>
                <td>${item.description}</td>
                <td><img src="${item.image_url}" alt="photo" class="contact-thumb" onerror="this.src='https://via.placeholder.com/50'"></td>
                <td>${item.phone}</td>
                <td>${item.email}</td>
            `;


            tr.addEventListener('click', (e) => {
                if (e.target.type !== 'checkbox') showDetails(item);
            });

            tableBody.appendChild(tr);
        });
    }

    function renderPagination() {
        paginationDiv.innerHTML = '';
        const pageCount = Math.ceil(filteredData.length / itemsPerPage);

        if (pageCount <= 1) return;

        for (let i = 1; i <= pageCount; i++) {
            const btn = document.createElement('button');
            btn.innerText = i;
            btn.className = `page-btn ${i === currentPage ? 'active' : ''}`;
            btn.addEventListener('click', () => {
                currentPage = i;
                renderTable();
                renderPagination();
            });
            paginationDiv.appendChild(btn);
        }
    }

    document.querySelectorAll('th.sortable').forEach(th => {
        th.addEventListener('click', () => {
            const column = th.dataset.column;
            if (currentSortColumn === column) {
                sortDirection *= -1;
            } else {
                currentSortColumn = column;
                sortDirection = 1;
            }

            document.querySelectorAll('.sort-indicator').forEach(sp => sp.innerText = '');
            th.querySelector('.sort-indicator').innerText = sortDirection === 1 ? ' ▲' : ' ▼';

            filteredData.sort((a, b) => {
                let valA = (a[column] || '').toString().toLowerCase();
                let valB = (b[column] || '').toString().toLowerCase();
                if (valA < valB) return -1 * sortDirection;
                if (valA > valB) return 1 * sortDirection;
                return 0;
            });

            renderTable();
            currentPage = 1;
            renderPagination();
        });
    });


    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            simulateAsyncOperation(() => {
                const query = searchInput.value.toLowerCase();
                filteredData = allData.filter(item =>
                    Object.values(item).some(val => String(val).toLowerCase().includes(query))
                );
                currentPage = 1;
                renderTable();
                renderPagination();
            });
        });
    }


    function showDetails(item) {
        if (!detailsBlock) return;
        detailsBlock.classList.remove('hidden');
        detailsContent.innerHTML = `
            <p><strong>ФИО:</strong> ${item.name}</p>
            <p><strong>Email:</strong> ${item.email}</p>
            <p><strong>Телефон:</strong> ${item.phone}</p>
            <p><strong>Описание:</strong> ${item.description}</p>
            ${item.image_url ? `<img src="${item.image_url}" style="max-width:200px;">` : ''}
        `;
    }


    const urlRegex = /^https?:\/\/.+(\.php|\.html)$/;
    const phoneRegex = /^(\+375|8)[\s-]?\(?\d{2,3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;

    function validateForm() {
        if (!inputUrl || !inputPhone) return;

        const isUrlValid = urlRegex.test(inputUrl.value);
        const isPhoneValid = phoneRegex.test(inputPhone.value);
        let valid = true;
        let msg = '';

        if (!isUrlValid && inputUrl.value.length > 0) {
            inputUrl.classList.add('invalid');
            msg += 'URL должен заканчиваться на .php или .html<br>';
            valid = false;
        } else {
            inputUrl.classList.remove('invalid');
        }

        if (!isPhoneValid && inputPhone.value.length > 0) {
            inputPhone.classList.add('invalid');
            msg += 'Телефон не валиден (8029... или +375...).';
            valid = false;
        } else {
            inputPhone.classList.remove('invalid');
        }

        if (validationMsg) validationMsg.innerHTML = msg;

        const allFilled = inputName.value && inputEmail.value && inputPhone.value && inputUrl.value;
        if (addEmployeeBtn) addEmployeeBtn.disabled = !(valid && allFilled);
    }

    if (inputUrl) {
        [inputUrl, inputPhone, inputName, inputEmail, inputDesc].forEach(el => {
            if (el) el.addEventListener('input', validateForm);
        });
    }


    if (addEmployeeBtn) {
        addEmployeeBtn.addEventListener('click', () => {
            simulateAsyncOperation(() => {
                const newContact = {
                    name: inputName.value,
                    description: inputDesc.value,
                    email: inputEmail.value,
                    phone: inputPhone.value,
                    image_url: inputUrl.value
                };

                allData.push(newContact);
                filteredData = [...allData];

                [inputName, inputDesc, inputEmail, inputPhone, inputUrl].forEach(i => i.value = '');
                addFormBlock.classList.add('hidden');
                toggleFormBtn.innerText = 'Добавить сотрудника';

                renderTable();
                renderPagination();
                alert('Сотрудник добавлен!');
            });
        });
    }


    if (bonusBtn) {
        bonusBtn.addEventListener('click', () => {
            simulateAsyncOperation(() => {
                const checkboxes = document.querySelectorAll('.select-row:checked');
                if (checkboxes.length === 0) {
                    bonusResult.innerText = "Никто не выбран.";
                    return;
                }
                const names = Array.from(checkboxes).map(cb => cb.value).join(', ');
                bonusResult.innerHTML = `<strong>Премированы сотрудники:</strong> ${names}.`;
            });
        });
    }
});