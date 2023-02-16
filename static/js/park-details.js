// JS for park details

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

        // const div = `
        //             <div> ${responseJson.result.shortDescription} </div>
        //             <div> ${responseJson.result.longDescription} </div>
        //             <div> <b> Location: </b> </div>
        //             <div> ${responseJson.result.location} </div>
        //             <div> <b> Activities: </b> </div> 
        //                 <ul> 
        //                 $(for activity in ${responseJson.result.activities}) {
        //                     <li> ${{ activity }} </li>
        //                 }                        
        //                 </ul>
        //             <div> <b> Topics: </b> </div> 
        //                 <ul> 
        //                 {%for topic in ${responseJson.result.activities} %}
        //                 <li> {{ activity }} </li>
        //                 {% endfor %}
        //                 </ul>
        //             <div> <b> Images: </b>
        //             {% for image in ${responseJson.result.images} %}
        //                 <img url= {{ image }}>
        //             `
        // html_string += div
        
        // document.querySelector(".result_attraction_details").innerHTML = html_string
   