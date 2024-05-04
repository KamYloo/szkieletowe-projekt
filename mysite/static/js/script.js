/**
 * Element podmenu.
 * @type {HTMLElement}
 */
let subMenu = document.getElementById("subMenu");

/**
 * Lista elementów opcji tematów.
 * @type {NodeList}
 */
const option_topics = document.querySelectorAll("#option_topic");

/**
 * Przełącza widoczność podmenu poprzez dodanie lub usunięcie klasy "open_menu".
 */
function toggleMenu() {
  subMenu.classList.toggle("open_menu");
}

/**
 * Dodaje nasłuchiwanie zdarzenia kliknięcia dla każdego elementu opcji tematów
 * i przełącza klasę "topic_seetings".
 */
option_topics.forEach((option_topic) => {
  option_topic.addEventListener("click", function () {
    option_topic.classList.toggle("topic_seetings");
  });
});

/**
 * Aktualizuje nazwę pliku wyświetlaną na stronie na podstawie wybranego pliku.
 * @param {HTMLInputElement} input - Element wejściowy pliku.
 */
function updateFileName(input) {
    var fileName = '';
    if (input.files && input.files.length > 0) {
        fileName = input.files[0].name;
    } else {
        fileName = 'Brak pliku wybranego';
    }
    document.getElementById('file-name-placeholder').innerText = fileName;
}
