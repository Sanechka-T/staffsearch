const burger = document.querySelector('#burger');
const menu = document.querySelector('#menu');
const overlay = document.querySelector('#overlay');

burger.addEventListener('click', () => {
    if (menu.classList.contains('click')) {
        menu.classList.remove('click');
        overlay.style.display = 'block'; // Скрыть затемнение
    } else {
        menu.classList.add('click');
        overlay.style.display = 'none'; // Показать затемнение
    }
});

// Скрытие меню и затемнения при клике на затемнение
overlay.addEventListener('click', () => {
    menu.classList.add('click');
    overlay.style.display = 'none'; // Скрыть затемнение
});
