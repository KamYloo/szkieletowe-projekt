const dropdows = document.querySelectorAll('.dropdown-menu');

dropdows.forEach(dropdow => {
    const select = dropdow.querySelector('.dropmenu-icon');
    const menu = dropdow.querySelector('.menu-list');

    select.addEventListener('click', ()=>{
        // select.classList.toggle('sele')
        menu.classList.toggle('menu-open');
    });
});