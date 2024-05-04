/**
 * Obsługuje kliknięcie na ikonę "paper-plane" w celu wysłania wiadomości.
 */
$('.fa-paper-plane').on('click', function() {
    $('#send_message_form').submit();
});

/**
 * Pole tekstowe dla wiadomości.
 * @type {jQuery}
 */
let input_message = $('#input_messages')

/**
 * Obszar, w którym wyświetlane są wiadomości.
 * @type {jQuery}
 */
let message_body = $('.msg_card_body')

/**
 * Formularz wysyłania wiadomości.
 * @type {jQuery}
 */
let send_message_form = $('#send_message_form')

/**
 * ID zalogowanego użytkownika.
 * @type {string}
 */
const USER_ID = $('#logged_in_user').val()

/**
 * Określa początek adresu URL WebSocket.
 * @type {string}
 */
let loc = window.location
let wsStart = 'ws://'
if(loc.protocol === 'https') {
    wsStart = 'ws://'
}

/**
 * Adres URL WebSocket.
 * @type {string}
 */
let endpoint = wsStart + loc.host + loc.pathname

/**
 * WebSocket używany do komunikacji w czasie rzeczywistym.
 * @type {WebSocket}
 */
var socket = new WebSocket(endpoint)

/**
 * Obsługuje otwarcie połączenia z WebSocket.
 * @param {Event} e - Obiekt zdarzenia.
 */
socket.onopen = async function(e){
    console.log('open', e)

    send_message_form.on('submit', function (e) {
    e.preventDefault()
    let message = input_message.val()
    let send_to = get_active_other_user_id()
    let thread_id = get_active_thread_id()

    let data = {
        'message': message,
        'send_by': USER_ID,
        'send_to': send_to,
        'thread_id': thread_id,
    }
    data = JSON.stringify(data)
    socket.send(data)
    $(this)[0].reset()
})
}

/**
 * Obsługuje otrzymanie wiadomości przez WebSocket.
 * @param {MessageEvent} e - Obiekt zdarzenia wiadomości.
 */
socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let send_by_id = data['send_by']
    let thread_id = data['thread_id']
    let userData = data['user_data'];
    newMessage(message, send_by_id, thread_id, userData)
}

/**
 * Obsługuje błąd w połączeniu z WebSocket.
 * @param {Event} e - Obiekt zdarzenia błędu.
 */
socket.onerror = async function(e){
    console.log('error', e)
}

/**
 * Obsługuje zamknięcie połączenia z WebSocket.
 * @param {CloseEvent} e - Obiekt zdarzenia zamknięcia.
 */
socket.onclose = async function(e){
    console.log('close', e)
}

/**
 * Dodaje nową wiadomość do okna czatu.
 * @param {string} message - Treść wiadomości.
 * @param {string} send_by_id - ID wysyłającego użytkownika.
 * @param {string} thread_id - ID wątku.
 * @param {Object} userData - Dane użytkownika.
 */
function newMessage(message, send_by_id, thread_id, userData) {
	if ($.trim(message) === '') {
		return false;
	}
    let message_element;
    let chat_id = 'chat_' + thread_id
    if (send_by_id == USER_ID) {
        message_element = `
			<div class="my_message">
                  <div class="message_content">
                      <h6>${userData.first_name} ${userData.last_name}</h6>
                      <div class="message">
                          <p>${message}</p>
                      </div>
                  </div>
                  <img src="${userData.profile_picture}" alt="">
              </div>
	    `
    }
    else {
        message_element = `
			 <div class="recipent_message">
                    <img src="${userData.profile_picture}" alt="">
                    <div class="message_content">
                        <h6>${userData.first_name} ${userData.last_name}</h6>
                        <div class="message">
                            <p>${message}</p>
                        </div>
                    </div>
                </div>
	    `
    }

	let message_body = $('.chat[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}

/**
 * Obsługuje kliknięcie na kontakt w liście kontaktów.
 */
$('.contact-li').on('click', function (){
    $('.contacts .actiive').removeClass('active')
    $(this).addClass('active')

    let chat_id = $(this).attr('chat-id')
    $('.chat.is_active').removeClass('is_active')
    $('.chat[chat-id="' + chat_id +'"]').addClass('is_active')
})

/**
 * Pobiera ID aktywnego innego użytkownika.
 * @returns {string} - ID innego użytkownika.
 */
function get_active_other_user_id() {
     let other_user_id = $('.chat.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

/**
 * Pobiera ID aktywnego wątku.
 * @returns {string} - ID wątku.
 */
function get_active_thread_id(){
    let chat_id = $('.chat.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}
