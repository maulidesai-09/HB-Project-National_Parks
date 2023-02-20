// JS for Search

// JS for selecting a park on the search page - Upon the change in park selection, 
// it gets the details of the selected park from the browser/ html and sends it to the server

const park_name_element = document.querySelector("#park-name")

park_name_element.addEventListener('change', (evt) => {
    evt.preventDefault()

    const selected_park_id = park_name_element.value
    let url = ""

    console.log(selected_park_id)

    if (selected_park_id == "Select a park..") {
        url = '/search'
    } else {
        // url = `/search/result?park_name=${selected_park_id}`
        url = `/parks/${selected_park_id}`
    }

    console.log(url)

    window.location.href = url
})


// JS for search by state using map - obtains state information from the browser/ html and sends it to the server

const state_map_element = document.querySelectorAll(".map-state")

for (const state of state_map_element) {
    state.addEventListener('click', (evt) => {
        evt.preventDefault()
    
        const selected_map_state = evt.target.getAttribute("alt")
        console.log(evt.target)
        console.log(selected_map_state)
    
        url = `/search/state_map_result?selected_map_state=${selected_map_state}`
    
        window.location.href = url
    
    })
}