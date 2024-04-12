let input_message = $('#input_messages')
let message_body = $('.msg_card_body')
let send_message_form = $('#send_message_form')
const USER_ID = $('#logged_in_user').val()

let loc = window.location
let wsStart = 'ws://'
if(loc.protocol === 'https') {

    wsStart = 'ws://'
}

let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

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

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let send_by_id = data['send_by']
    let thread_id = data['thread_id']
    let userData = data['user_data'];
    newMessage(message, send_by_id, thread_id, userData)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}


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

$('.contact-li').on('click', function (){
    $('.contacts .actiive').removeClass('active')
    $(this).addClass('active')

    let chat_id = $(this).attr('chat-id')
    $('.chat.is_active').removeClass('is_active')
    $('.chat[chat-id="' + chat_id +'"]').addClass('is_active')

})

function get_active_other_user_id() {
     let other_user_id = $('.chat.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.chat.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}