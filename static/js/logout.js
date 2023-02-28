// JS for logout

const logout = document.querySelector("#logout");

logout.addEventListener('click', (evt) => {
    evt.preventDefault();

    let confirmation = null

    if (confirm("Are you sure you want to logout") === true) {
        confirmation = "Yes";
    } else {
        confirmation = "No";
    }

    const url= `/logout?confirmation=${confirmation}`

    window.location.href = url
})
    

    
