/**
 * Lista  menu rozwijanego na stronie przy rozdzielczosci mobilnej .
 * @type {NodeList}
 */
const dropdows = document.querySelectorAll('.dropdown-menu');

/**
 * Dodaje nasłuchiwanie zdarzenia kliknięcia dla każdego menu rozwijanego.
 */
dropdows.forEach(dropdow => {
    /**
     * Ikona menu rozwijanego.
     * @type {HTMLElement}
     */
    const select = dropdow.querySelector('.dropmenu-icon');

    /**
     * Lista opcji menu rozwijanego.
     * @type {HTMLElement}
     */
    const menu = dropdow.querySelector('.menu-list');

    /**
     * Obsługuje zdarzenie kliknięcia na ikonę menu rozwijanego.
     * Po kliknięciu przełącza widoczność opcji menu.
     */
    select.addEventListener('click', ()=>{
        menu.classList.toggle('menu-open');
    });
});
