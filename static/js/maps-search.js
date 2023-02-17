// JS for Google Maps to be displayed on Advance Search Results page

function initMap() {

    // const parkLat = parseFloat(document.querySelector("#lat").innerHTML)
    // const parkLong = parseFloat(document.querySelector("#long").innerHTML)
    // const parkName = document.querySelector("#park_name").innerHTML

    let locations = []

    for (const park of document.querySelectorAll(".result-park")) {
        const park_details = {}
        const park_coords = {}
        park_details['name'] = park.getElementsByTagName("a")[0].innerHTML
        park_details['hyperlink'] = park.getElementsByTagName("a")[0].href
        park_coords['lat'] = parseFloat(park.getElementsByClassName("lat")[0].innerHTML)
        park_coords['lng'] = parseFloat(park.getElementsByClassName("long")[0].innerHTML)
        park_details['coords'] = park_coords

        locations.push(park_details)
    }

    let average_latitude = undefined
    let average_longitude = undefined
    
    let latitudes = []
    for (const park of document.querySelectorAll(".result-park")) {
        latitudes.push(parseFloat(park.getElementsByClassName("lat")[0].innerHTML))
    }
    
    if (latitudes.length === 0) {
        average_latitude = 47.116386
    } else {
        average_latitude = (Math.min(...latitudes) + Math.max(...latitudes))/2
    }
    

    let longitudes = []
    for (const park of document.querySelectorAll(".result-park")) {
        longitudes.push(parseFloat(park.getElementsByClassName("long")[0].innerHTML))}
    
    if (longitudes.length === 0) {
        average_longitude = -101.299591
    } else {
        average_longitude = (Math.min(...longitudes) + Math.max(...longitudes))/2
    }

    
    let basicMap = new google.maps.Map(document.querySelector("#map"), {
        center: {
            lat: average_latitude,
            lng: average_longitude,
          },
        zoom: 3.5
    }
    );


    const markers = []
    for (const location of locations) {
        markers.push(
            new google.maps.Marker({
                position: location.coords,
                title: `<a href="${location.hyperlink}"> ${location.name} </a>`,
                map: basicMap
            })
        )
    }


    for (const marker of markers) {
        const markerInfo = `${marker.title}`

        // <p>
        //     Located at: <code> ${marker.position.lat} </code>,
        //     Located at: <code> ${marker.position.lng} </code>,
        // </p>
        // `
        const infoWindow = new google.maps.InfoWindow({
            content: markerInfo,
            maxWidth: 200
        });
    
    
        marker.addListener('click', () => {
            infoWindow.open(basicMap, marker);
        });
    }

// AJAX - Search for park by State, by Activities and by Topics:

const advance_search_element = document.querySelector("#search-button")
const advance_clear_element = document.querySelector("#clear")
const park_state_element = document.querySelector(".state-name")
const park_activities_element = document.querySelectorAll(".checkbox-activity")
const park_topics_element = document.querySelectorAll(".checkbox-topic")

advance_search_element.addEventListener('click', (evt) => {
    evt.preventDefault()

    const park_state = park_state_element.value
    console.log(park_state)
    
    const park_activities = []
    for (const activity of park_activities_element) {
        if (activity.checked) {
            park_activities.push(activity.value)
        }
    }

    const park_topics = []
    for (const topic of park_topics_element) {
        console.log(topic.value)
        if (topic.checked) {
            park_topics.push(topic.value)
        }
    }

    const formInputs = {'state': park_state,
                    'activities': park_activities,
                    'topics': park_topics}
    
    fetch('/api/search/advance_search_result/ajax', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    
        .then((response) => response.json())  // becomes response.json()
        .then((responseJson) => {
            // if (responseJson.response) {
            //     // create HTML string
            //     // for loop
            //         // for each park, create <li> using a template string and append to HTML string
            //     // innerHTML = HTML string

            //     // clear existing markers and use code above to make new markers based on results from ajax call and recenter the map
            // }
            // else {
            //     // display "No parks"
            // }

            if (responseJson.response) {
                let html_string = ""

                for (const park of responseJson.result) {
                    const li = `<li> <a href="/parks/${park.park_id}"> ${park.park_name} </a></li>`
                    html_string += li
                }
                console.log(html_string)
                document.querySelector(".result").innerHTML = html_string

                // for (const park of responseJson.response) {
                    
                // }


                let locations = []
                for (const park of responseJson.result) {
                    park_details = {}
                    park_coords ={}
                    park_details['name'] = park.park_name
                    park_details['hyperlink'] = `/parks/${park.park_id}`
                    park_coords['lat'] = parseFloat(park.park_lat)
                    park_coords['lng'] = parseFloat(park.park_long)
                    park_details['coords'] = park_coords

                    locations.push(park_details)
                }

                for (const marker of markers) {
                    marker.setMap(null)
                }

                latitudes = []
                for (const park of responseJson.result) {
                    latitudes.push(parseFloat(park.park_lat))
                }
                
                average_latitude = (Math.min(...latitudes) + Math.max(...latitudes))/2
                

                longitudes = []
                for (const park of responseJson.result) {
                    longitudes.push(parseFloat(park.park_long))}
                
                average_longitude = (Math.min(...longitudes) + Math.max(...longitudes))/2
                
                

                basicMap = new google.maps.Map(document.querySelector("#map"), {
                    center: {
                        lat: average_latitude,
                        lng: average_longitude,
                      },
                    zoom: 4
                })

                // Using 'const markers' instead of 'let markers' on line 49 because using 'let markers' 
                // does not create new markers in the code below even after reassigning makers = [].
                // Hence, using markers.length = 0 below to empty the markers list 

                markers.length = 0
                for (const location of locations) {
                    markers.push(
                        new google.maps.Marker({
                            position: location.coords,
                            title: `<a href="${location.hyperlink}"> ${location.name} </a>`,
                            map: basicMap
                        })
                    )
                }

                
                for (const marker of markers) {
                    const markerInfo = `${marker.title}`

                    // <p>
                    //     Located at: <code> ${marker.position.lat} </code>,
                    //     Located at: <code> ${marker.position.lng} </code>,
                    // </p>
                    // `
                    const infoWindow = new google.maps.InfoWindow({
                        content: markerInfo,
                        maxWidth: 200
                    });
                
                
                    marker.addListener('click', () => {
                        infoWindow.open(basicMap, marker);
                    });
                }
            } else {
                document.querySelector(".result").innerHTML = responseJson.result

                // let locations = []
                // for (const park of responseJson.result) {
                //     park_details = {}
                //     park_coords ={}
                //     park_details['name'] = park.park_name
                //     park_details['hyperlink'] = `/parks/${park.park_id}`
                //     park_coords['lat'] = parseFloat(park.park_lat)
                //     park_coords['lng'] = parseFloat(park.park_long)
                //     park_details['coords'] = park_coords

                //     locations.push(park_details)
                // }

                for (const marker of markers) {
                    marker.setMap(null)
                }

                // latitudes = []
                // for (const park of responseJson.result) {
                //     latitudes.push(parseFloat(park.park_lat))
                // }
                
                // if (latitudes.length === 0) {
                average_latitude = 47.116386
                // } else {
                // average_latitude = (Math.min(...latitudes) + Math.max(...latitudes))/2
                // }
                
                

                // longitudes = []
                // for (const park of responseJson.result) {
                //     longitudes.push(parseFloat(park.park_long))}
                
                // if (longitudes.length === 0) {
                average_longitude = -101.299591
                // } else {
                //     average_longitude = (Math.min(...longitudes) + Math.max(...longitudes))/2
                // }
                
                // console.log(latitudes)
                // console.log(longitudes)
                console.log(average_latitude)
                console.log(average_longitude)

                basicMap = new google.maps.Map(document.querySelector("#map"), {
                    center: {
                        lat: average_latitude,
                        lng: average_longitude,
                      },
                    zoom: 4
                })

                // Using 'const markers' instead of 'let markers' on line 49 because using 'let markers' 
                // does not create new markers in the code below even after reassigning makers = [].
                // Hence, using markers.length = 0 below to empty the markers list 

                // markers.length = 0
                // for (const location of locations) {
                //     markers.push(
                //         new google.maps.Marker({
                //             position: location.coords,
                //             title: `<a href="${location.hyperlink}"> ${location.name} </a>`,
                //             map: basicMap
                //         })
                //     )
                // }


            }


                

            // document.querySelector(".result").innerHTML = responseText
        //     `{% if ${responseJson.response} == true %}
        //     <ul>
        //         {% for ind_result in ${responseJson.result} %}
        //             <li> {{ ind_result.park_name }} </li>
        //         {% endfor %}
        //     </ul>
        // {% else %}
        //     <p> ${responseJson.result} </p>
        // {% endif %}`

            


        })          
})
}