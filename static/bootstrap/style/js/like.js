const like = document.querySelector(".like")
let heart = document.getElementById("heart")

like.addEventListener("click",function(){
    let carId = this.dataset.carId;
    let url = this.dataset.url
    fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "car_id=" + carId
    })
    .then(res => res.json())
        .then(data => {
            heart.src = data.favorited ? heart.dataset.red : heart.dataset.black;
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}