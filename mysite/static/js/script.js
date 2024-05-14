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


document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".slider img");
    const slideCount = slides.length;
    let currentIndex = 0;

    function showSlide(index) {
      if (index < 0 || index >= slideCount) return;
      slides.forEach(slide => {
        slide.style.display = "none";
      });
      slides[index].style.display = "block";
      currentIndex = index;
    }

    function nextSlide() {
      currentIndex = (currentIndex + 1) % slideCount;
      showSlide(currentIndex);
    }

    setInterval(nextSlide, 6000);
  });


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
