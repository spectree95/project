const input = document.getElementById("chat-input");
const carId = parseInt(input.dataset.carId);
const carOwnerId = input.dataset.carOwnerId;
const currentUserId = input.dataset.currentUserId
const send_to_owner = document.getElementById("send_to_owner")

const ws = new WebSocket(`ws://${location.host}/ws/chat_owner/${carId}/`);

const messageContainer = document.getElementById("messages");
const sendBtn = document.getElementById("message-send");

ws.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageEl = document.createElement("div");
    messageEl.classList.add("message");
    if (data.sender_name == currentUserId) {
        messageEl.classList.add("my-message")
    }
    else {
        messageEl.classList.add("other-message")
    }
    messageEl.textContent = `${data.message}`
    messageContainer.appendChild(messageEl)
    messageContainer.scrollTop = messageContainer.scrollHeight
}

console.log("carId = ", carId, "typeof:", typeof carId);
sendBtn.onclick = function () {
    const message = input.value;
    if (!message) return;
    ws.send(JSON.stringify({
        "command": "send",
        "message": message,
        "sender_id": currentUserId,
        "car_id": carId,
        
    }));

    input.value = "";

};

input.addEventListener("keyup", function(e){
    if (e.key == "Enter"){
        sendBtn.click()
    }
})
