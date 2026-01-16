document.addEventListener('DOMContentLoaded', () => {
    const toys = document.querySelectorAll('.toy-item');
    const belt = document.getElementById('belt');
    const machine = document.querySelector('.packing-machine');

    let screenWidth = window.innerWidth;


    const finishLine = screenWidth - 250;

    window.addEventListener('resize', () => {
        screenWidth = window.innerWidth;
    });

    function updateFactory() {
        const scrollY = window.scrollY;


        belt.style.backgroundPosition = `-${scrollY}px 0`;


        toys.forEach((toy) => {
            const speed = parseFloat(toy.getAttribute('data-speed'));
            const offset = parseInt(toy.getAttribute('data-offset'));

            let currentX = (scrollY * speed) + offset;

            toy.style.left = `${currentX}px`;


            toy.style.transform = `rotate(${currentX / 2}deg)`;


            if (currentX > finishLine) {

                toy.style.opacity = `${1-(currentX**2/10000000)*3}`;
                toy.style.transform = `scale(0.4) rotate(${currentX}deg)`;
            } else {
                toy.style.opacity = '1';

            }
        });
    }


    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateFactory();
                ticking = false;
            });
            ticking = true;
        }
    });

    updateFactory();
});