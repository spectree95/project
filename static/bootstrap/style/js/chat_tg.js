const input = document.getElementById("chat-input");
const carId = input.dataset.carId
const userId = input.dataset.userId
const currentUserId = input.dataset.currentUserId


document.querySelector(".chat_user").forEach(el => {
    el.addEventListener("click", ()=>{
        const other_user_id = el.dataset.userrid
    })
});

const ws = new WebSocket(`ws://${location.host}/ws/chat/${carId}/`);
const messagesContainer = document.getElementById("chat-messages");
const sendBtn = document.getElementById("chat-send");



ws.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageEl = document.createElement("div");
    messageEl.classList.add("message")
    if (data.sender_id==currentUserId) {
        messageEl.classList.add("message-sent");
    }
    else{
        messageEl.classList.add("message-received");
    }
    messageEl.textContent = `${data.message}`;
    messagesContainer.appendChild(messageEl)
    messagesContainer.scrollTop = messagesContainer.scrollHeight
};



sendBtn.onclick = function() {
    const message = input.value;
    if (!message) return;

    ws.send(JSON.stringify({
        "message": message,
        "sender_id": currentUserId,
    }));

    input.value = ""; // очистка поля ввода
};

input.addEventListener("keyup", function(e) {
    if (e.key=="Enter"){
        sendBtn.click()
    }
})