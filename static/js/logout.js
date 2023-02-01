// JS for logout

const logout = document.querySelector("#logout");

logout.addEventListener('click', (evt) => {
    evt.preventDefault();

    // confirm("Are you sure you want to logout")

    let confirmation = null

    if (confirm("Are you sure you want to logout") === true) {
        confirmation = "Yes";
    } else {
        confirmation = "No";
    }

    const url= `/logout?confirmation=${confirmation}`

    fetch(url)
    .then((response) => response.text())
    .then((message) => {
        alert(message)
    })
})
    

    
