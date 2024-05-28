/**
 * Adres URL bieżącej strony internetowej.
 * @type {string}
 */
const url = window.location.href

/**
 * Formularz wyszukiwania.
 * @type {HTMLElement}
 */
const searchForm = document.getElementById('search_form')

/**
 * Pole wprowadzania tekstu wyszukiwania.
 * @type {HTMLElement}
 */
const searchInput = document.getElementById('search_thread_input')

/**
 * Kontener na wyniki wyszukiwania.
 * @type {HTMLElement}
 */
const resultsBox = document.getElementById('results_box')

/**
 * Token CSRF używany do zabezpieczenia przed atakami CSRF.
 * @type {string}
 */
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

/**
 * Wysyła dane wyszukiwania za pomocą żądania AJAX.
 * @param {string} users - Wprowadzone przez użytkownika wyszukiwanie.
 */
const sendSearchData = (users) => {
    $.ajax({
        type: 'POST',
        url: 'search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'users': users,
        },
        success: (res) => {
            console.log(res.data)
            const data = res.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(users => {
                    resultsBox.innerHTML += `
                    <ul>
                      <a href="${url}create_thread/${users.pk}/">
                        <img src="${users.avatar}" alt="">
                        <p>${users.first_name} ${users.last_name}</p>
                      </a>
                    </ul>
                    `
                })
            }
            else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<b>${data}</b>`
                }
                else {
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}

/**
 * Obsługuje zdarzenie wciśnięcia klawisza podczas wprowadzania tekstu wyszukiwania.
 * @event keyup
 * @memberof HTMLInputElement
 * @name searchInput
 * @param {KeyboardEvent} e - Obiekt zdarzenia klawisza.
 */
searchInput.addEventListener('keyup', e=> {
    console.log(e.target.value)

    if (resultsBox.classList.contains('not-visible')) {
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})
