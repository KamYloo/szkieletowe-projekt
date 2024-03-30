const selectBtn1 = document.getElementById('select-btn1');
const selectBtn2 = document.getElementById('select-btn2');
const text1 = document.getElementById('text text1');
const text2 = document.getElementById('text text2');
const option1 = document.getElementsByClassName('option option1');
const option2 = document.getElementsByClassName('option option2');
let subMenu = document.getElementById("subMenu");
const option_topics = document.querySelectorAll("#option_topic");
function toggleMenu() {
  subMenu.classList.toggle("open_menu");
}

option_topics.forEach((option_topic) => {
  option_topic.addEventListener("click", function () {
    option_topic.classList.toggle("topic_seetings");
  });
});

function updateFileName(input) {
        var fileName = '';
        if (input.files && input.files.length > 0) {
            fileName = input.files[0].name;
        } else {
            fileName = 'Brak pliku wybranego';
        }
        document.getElementById('file-name-placeholder').innerText = fileName;
    }

selectBtn1.addEventListener('click', function() {
    selectBtn1.classList.toggle('active');
})

selectBtn2.addEventListener('click', function() {
    selectBtn2.classList.toggle('active');
})

for (options of option1) {
    options.onclick = function() {
        text1.innerHTML = this.textContent;
        selectBtn = classList.remove('active');
    }
}


for (options of option2) {
    options.onclick = function() {
        text2.innerHTML = this.textContent;
    }
}




