// JS for Date formatting for trip details


// for restricting selection of dates prior to today's date
date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1; //month starts from 0
day = date.getDate();

if(month<10) month = "0" + month;
if (day<10) day = "0" + day;
today = year + "-" + month + "-" + day;

document.querySelector("#start-date").setAttribute('min', today)
document.querySelector("#end-date").setAttribute('min', today)




// for providing main attractions to be displayed based on park selected on plan_trip.html

let park_element = document.querySelector("#park-name")

park_element.addEventListener('change', (evt) => {
    evt.preventDefault()

    const selected_park_id = park_element.value
    console.log(park_element)
    console.log(selected_park_id)

    const url = `/app/plan-trip/ajax?park_id=${selected_park_id}`

    fetch(url)
    .then((response) => response.text())
    .then((responseText) => {
        document.querySelector(".trip-things-dropdown").innerHTML = responseText
        console.log(responseText)
    })
})






