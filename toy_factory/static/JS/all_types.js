document.addEventListener('DOMContentLoaded', () => {

    const xStartInp = document.getElementById('x-start');
    const xEndInp = document.getElementById('x-end');
    const xStepInp = document.getElementById('x-step');
    const epsilonInp = document.getElementById('epsilon');
    const btnDraw = document.getElementById('btn-draw');
    const btnSave = document.getElementById('btn-save-chart');
    const tableBody = document.querySelector('#math-table tbody');
    const tableContainer = document.querySelector('.table-scroll-container');

    let myChart = null;


    function calculateSeries(x, eps) {
        let sum = 0;
        let n = 0;
        let term;
        const maxIter = 1000;
        do {
            const power = 2 * n + 1;
            term = 1 / (power * Math.pow(x, power));
            sum += term;
            n++;
        } while (Math.abs(2 * term) > eps && n < maxIter);
        return { value: 2 * sum, iterations: n };
    }

    function drawChart() {
        console.log("Начало построения графика...");

        const xStart = parseFloat(xStartInp.value);
        const xEnd = parseFloat(xEndInp.value);
        const step = parseFloat(xStepInp.value);
        const eps = parseFloat(epsilonInp.value);


        if (Math.abs(xStart) <= 1) {
            alert("Ошибка: Аргумент X должен быть по модулю больше 1 (|x|>1)!");
            return;
        }
        if (step <= 0) {
            alert("Ошибка: Шаг должен быть больше 0!");
            return;
        }
        if (xStart >= xEnd) {
            alert("Ошибка: Начало X должно быть меньше Конца X!");
            return;
        }

        const labels = [];
        const dataSeries = [];
        const dataMath = [];


        if (tableBody) tableBody.innerHTML = '';


        let count = 0;
        const maxPoints = 2000;

        for (let x = xStart; x <= xEnd; x += step) {
            if (count > maxPoints) {
                alert("Слишком много точек! Увеличьте шаг.");
                break;
            }

            let currentX = parseFloat(x.toFixed(2));


            const mathVal = Math.log((currentX + 1) / (currentX - 1));
            const seriesResult = calculateSeries(currentX, eps);


            labels.push(currentX);
            dataSeries.push(seriesResult.value);
            dataMath.push(mathVal);


            if (tableBody) {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${currentX}</td>
                    <td>${seriesResult.iterations}</td>
                    <td>${seriesResult.value.toFixed(5)}</td>
                    <td>${mathVal.toFixed(5)}</td>
                    <td>${Math.abs(mathVal - seriesResult.value).toExponential(2)}</td>
                `;
                tableBody.appendChild(tr);
            }
            count++;
        }


        if (tableContainer) tableContainer.style.display = 'block';


        if (myChart) {
            myChart.destroy();
            myChart = null;
        }

        const canvas = document.getElementById('myChart');
        if (!canvas) {
            console.error("Canvas не найден!");
            return;
        }
        const ctx = canvas.getContext('2d');


        const totalDuration = 1500;
        const delayBetweenPoints = totalDuration / dataSeries.length;

        const progressiveAnimation = {
            x: {
                type: 'number',
                easing: 'linear',
                duration: delayBetweenPoints,
                from: NaN,
                delay(ctx) {
                    if (ctx.type !== 'data' || ctx.xStarted) {
                        return 0;
                    }
                    ctx.xStarted = true;
                    return ctx.index * delayBetweenPoints;
                }
            }
        };


        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Ряд Тейлора F(x)',
                        data: dataSeries,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    },
                    {
                        label: 'Math.log F(x)',
                        data: dataMath,
                        borderColor: 'rgb(54, 162, 235)',
                        borderDash: [5, 5],
                        borderWidth: 2,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                animation: progressiveAnimation,
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Значение X' }
                    },
                    y: {
                        title: { display: true, text: 'Значение F(x)' }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'График функции ln((x+1)/(x-1))',
                        font: { size: 16 }
                    }
                }
            }
        });

        console.log("График построен успешно.");
    }


    if(btnDraw) btnDraw.addEventListener('click', drawChart);

    if(btnSave) btnSave.addEventListener('click', () => {
        if(!myChart) { alert('График не построен'); return; }
        const link = document.createElement('a');
        link.href = myChart.toBase64Image();
        link.download = 'chart.png';
        link.click();
    });

    if(document.getElementById('myChart')) {
        setTimeout(drawChart, 100);
    }


    const triggerCheckbox = document.getElementById('create-radio-trigger');
    const workspace = document.getElementById('workspace');
    const clearBtn = document.getElementById('clear-storage-btn');
    const STORAGE_KEY = 'radio_gen_data';
    let radioElements = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

    function saveState() { localStorage.setItem(STORAGE_KEY, JSON.stringify(radioElements)); }
    function generateId() { return '_' + Math.random().toString(36).substr(2, 9); }

    function renderItem(itemData) {
        const card = document.createElement('div');
        card.className = 'radio-card';
        card.dataset.id = itemData.id;
        card.innerHTML = `
            <div class="settings-panel">
                <input type="text" class="input-name" value="${itemData.name}" placeholder="Name">
                <input type="text" class="input-value" value="${itemData.value}" placeholder="Value">
                <label class="checkbox-attr"><input type="checkbox" class="input-checked" ${itemData.checked ? 'checked' : ''}> Checked</label>
                <label class="checkbox-attr"><input type="checkbox" class="input-required" ${itemData.required ? 'checked' : ''}> Required</label>
                <label class="checkbox-attr"><input type="checkbox" class="input-disabled" ${itemData.disabled ? 'checked' : ''}> Disabled</label>
            </div>
            <div class="preview-panel">
                <span class="preview-label">Результат</span>
                <div class="generated-element-wrapper">
                    <input type="radio" name="${itemData.name}" value="${itemData.value}"
                        ${itemData.checked ? 'checked' : ''} ${itemData.required ? 'required' : ''} ${itemData.disabled ? 'disabled' : ''}>
                    <span>${itemData.value || 'Radio'}</span>
                </div>
            </div>
            <button class="delete-item-btn" title="Удалить">×</button>
        `;
        const inputs = card.querySelectorAll('input:not([type="radio"])');
        inputs.forEach(input => input.addEventListener('input', (e) => updateItem(itemData.id, e.target)));
        card.querySelector('.delete-item-btn').addEventListener('click', () => deleteItem(itemData.id));
        return card;
    }

    function renderAll() {
        if(!workspace) return;
        workspace.innerHTML = '';
        radioElements.forEach(item => workspace.appendChild(renderItem(item)));
    }

    function addNewRadio() {
        const newItem = { id: generateId(), name: 'delivery', value: 'opt-' + (radioElements.length + 1), checked: false, required: false, disabled: false };
        radioElements.push(newItem); saveState(); workspace.appendChild(renderItem(newItem));
    }

    function updateItem(id, el) {
        const item = radioElements.find(i => i.id === id);
        if(!item) return;
        if(el.classList.contains('input-name')) item.name = el.value;
        if(el.classList.contains('input-value')) item.value = el.value;
        if(el.classList.contains('input-checked')) item.checked = el.checked;
        if(el.classList.contains('input-required')) item.required = el.checked;
        if(el.classList.contains('input-disabled')) item.disabled = el.checked;
        saveState();
        const card = document.querySelector(`.radio-card[data-id="${id}"]`);
        const rb = card.querySelector('input[type="radio"]');
        rb.name = item.name; rb.value = item.value; rb.checked = item.checked; rb.required = item.required; rb.disabled = item.disabled;
        card.querySelector('.generated-element-wrapper span').textContent = item.value || 'Radio';
    }

    function deleteItem(id) { radioElements = radioElements.filter(i => i.id !== id); saveState(); renderAll(); }

    if(triggerCheckbox) triggerCheckbox.addEventListener('change', function() { if(this.checked) { addNewRadio(); setTimeout(() => { this.checked = false; }, 200); } });
    if(clearBtn) clearBtn.addEventListener('click', () => { if(confirm('Очистить?')) { radioElements = []; saveState(); renderAll(); } });
    renderAll();


    const residentsTableBody = document.querySelector('#residents-table tbody');
    const resultBox = document.getElementById('oop-result');
    let residentsArray = [];

    class AddressBase {
        constructor(street, house, apartment) { this._street = street; this._house = house; this._apartment = apartment; }
        get fullAddress() { return `ул. ${this._street}, д. ${this._house}, кв. ${this._apartment}`; }
        isSameAddress(other) { return this._street.toLowerCase() === other._street.toLowerCase() && this._house === other._house && this._apartment === other._apartment; }
    }

    class ResidentClass extends AddressBase {
        constructor(surname, city, street, house, apartment) { super(street, house, apartment); this._surname = surname; this._city = city; }
        get surname() { return this._surname; }
        get city() { return this._city; }

        static createFromForm() {
            const s = document.getElementById('res-surname').value;
            const c = document.getElementById('res-city').value;
            const st = document.getElementById('res-street').value;
            const h = document.getElementById('res-house').value;
            const a = document.getElementById('res-apt').value;
            if(!s || !c || !st || !h || !a) { alert('Заполните поля'); return null; }
            return new ResidentClass(s, c, st, h, a);
        }

        static displayAll(arr) {
            if(!residentsTableBody) return;
            residentsTableBody.innerHTML = '';
            arr.forEach(r => {
                const tr = document.createElement('tr');
                const sn = r.surname || (r.getSurname ? r.getSurname() : '');
                const ct = r.city || (r.getCity ? r.getCity() : '');
                const ad = r.fullAddress || (r.getFullAddress ? r.getFullAddress() : '');
                tr.innerHTML = `<td>${sn}</td><td>${ct}</td><td>${ad}</td>`;
                residentsTableBody.appendChild(tr);
            });
        }

        static solveTask(arr) {
            let res = [];
            for (let i = 0; i < arr.length; i++) {
                for (let j = i + 1; j < arr.length; j++) {
                    const p1 = arr[i]; const p2 = arr[j];
                    const c1 = p1.city || p1.getCity(); const c2 = p2.city || p2.getCity();
                    const sameAddr = (p1.isSameAddress) ? p1.isSameAddress(p2) : false;

                    if (c1.toLowerCase() !== c2.toLowerCase() && sameAddr) {
                        const s1 = p1.surname || p1.getSurname();
                        const s2 = p2.surname || p2.getSurname();
                        res.push(`${s1} (${c1}) и ${s2} (${c2})`);
                    }
                }
            }
            return res;
        }
    }

    function AddressProto(s, h, a) { this._street = s; this._house = h; this._apartment = a; }
    AddressProto.prototype.getFullAddress = function() { return `ул. ${this._street}, д. ${this._house}, кв. ${this._apartment}`; };
    AddressProto.prototype.isSameAddress = function(o) { return this._street.toLowerCase() === o._street.toLowerCase() && this._house === o._house && this._apartment === o._apartment; };
    function ResidentProto(sn, c, s, h, a) { AddressProto.call(this, s, h, a); this._surname = sn; this._city = c; }
    ResidentProto.prototype = Object.create(AddressProto.prototype);
    ResidentProto.prototype.constructor = ResidentProto;
    ResidentProto.prototype.getSurname = function() { return this._surname; };
    ResidentProto.prototype.getCity = function() { return this._city; };


    if(document.getElementById('btn-add-resident')) {
        residentsArray = [
            new ResidentClass("Иванов", "Витебск", "Ленина", "10", "5"),
            new ResidentClass("Петров", "Полоцк", "Ленина", "10", "5"),
            new ResidentClass("Сидоров", "Орша", "Мира", "1", "1")
        ];
        ResidentClass.displayAll(residentsArray);

        document.getElementById('btn-add-resident').addEventListener('click', () => {
            const mode = document.querySelector('input[name="logic-mode"]:checked').value;
            let newItem = (mode === 'class') ? ResidentClass.createFromForm() :
                new ResidentProto(
                    document.getElementById('res-surname').value,
                    document.getElementById('res-city').value,
                    document.getElementById('res-street').value,
                    document.getElementById('res-house').value,
                    document.getElementById('res-apt').value
                );
            if(newItem) {
                residentsArray.push(newItem);
                document.querySelectorAll('#resident-form input').forEach(i => i.value = '');
                ResidentClass.displayAll(residentsArray);
            }
        });

        document.getElementById('btn-show-all').addEventListener('click', () => ResidentClass.displayAll(residentsArray));

        document.getElementById('btn-solve').addEventListener('click', () => {
            const matches = ResidentClass.solveTask(residentsArray);
            if (matches.length > 0) {
                resultBox.innerHTML = "<b>Найдены совпадения:</b><br>" + matches.join('<br>');
                resultBox.classList.remove('hidden');
            } else {
                resultBox.innerHTML = "Совпадений не найдено.";
                resultBox.classList.remove('hidden');
            }
        });
    }


    const btnGeo = document.getElementById('btn-get-geo');
    const geoOutput = document.getElementById('geo-output');

    if (btnGeo) {
        btnGeo.addEventListener('click', () => {
            geoOutput.innerHTML = '🔍 Сканирование...';
            geoOutput.classList.remove('hidden');

            if (!navigator.geolocation) {
                geoOutput.textContent = 'Геолокация недоступна.';
                return;
            }

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const lat = position.coords.latitude.toFixed(6);
                    const lng = position.coords.longitude.toFixed(6);
                    const accuracy = position.coords.accuracy;

                    let ipData = 'Неизвестно';
                    try {
                        const res = await fetch('https://api.ipify.org?format=json');
                        const json = await res.json();
                        ipData = json.ip;
                    } catch (e) {}

                    const mapUrl = `https://www.google.com/maps?q=${lat},${lng}`;

                    geoOutput.innerHTML = `
                        <h3 style="color: #d63031; margin-top:0;">НАШЕЛ!</h3>
                        <div style="text-align: left; font-family: monospace; font-size: 0.9em; margin-bottom: 10px;">
                            <strong>📍 Коорд:</strong> ${lat}, ${lng} (±${accuracy}м)<br>
                            <strong>🌐 IP:</strong> ${ipData}<br>
                            <strong>🖥️ Экран:</strong> ${window.screen.width}x${window.screen.height}<br>
                            <strong>🕵️ Браузер:</strong> ${navigator.userAgent.slice(0, 50)}...<br>
                        </div>
                        <a href="${mapUrl}" target="_blank" class="submit-btn" style="background:#0984e3; text-decoration:none; display:inline-block; color:white; padding:5px 10px;">
                            🗺️ Показать на карте
                        </a>
                    `;
                    geoOutput.style.border = '2px solid #d63031';
                    geoOutput.style.background = '#fff0f0';
                },
                (err) => {
                    geoOutput.innerHTML = `<span style="color:red">Ошибка: ${err.message}</span>`;
                }
            );
        });
    }

    const btnSpeak = document.getElementById('btn-speak-task');
    if(btnSpeak) {
        btnSpeak.addEventListener('click', () => {
             const txt = document.querySelector('.task-desc').innerText;
             if('speechSynthesis' in window) {
                 const u = new SpeechSynthesisUtterance(txt);
                 u.lang = 'ru-RU';
                 window.speechSynthesis.speak(u);
             }
        });
    }

    if ('getBattery' in navigator) {
        navigator.getBattery().then((battery) => {
            function update() {
                const l = Math.round(battery.level * 100) + '%';
                const t = document.getElementById('battery-text');
                const f = document.getElementById('battery-fill');
                if(t && f) {
                    t.innerText = l + (battery.charging ? ' ⚡' : '');
                    f.style.width = l;
                    f.style.background = (battery.level < 0.2) ? '#d63031' : '#00b894';
                }
            }
            update();
            battery.addEventListener('levelchange', update);
            battery.addEventListener('chargingchange', update);
        });
    }
});