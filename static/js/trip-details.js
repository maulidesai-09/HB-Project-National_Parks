// JS for trip details

const attractions = document.querySelectorAll(".attraction")

console.log(attractions)

for (const attraction of attractions) {
    attraction.addEventListener('click', (evt) => {
        evt.preventDefault()

        const attraction_id = attraction.id
        console.log(attraction_id)

        const attraction_title = attraction.innerHTML.trim()
        id = document.querySelector("#park_id").innerHTML


        url = `/api/parks/${id}/main-attractions/ajax?title=${attraction_title}`
        
        fetch(url)
        .then((response) => response.text())
        .then((responseText) => {document.querySelector(`#result_${attraction_id}`).innerHTML = responseText
        })
    })
    }