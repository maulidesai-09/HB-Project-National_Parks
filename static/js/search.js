// JS for Search

const park_name_element = document.querySelector("#park-name")

// park_name_element.addEventListener('change', (evt) => {
//     evt.preventDefault()

//     const selected_park_name = park_name_element.value
//     let url = ""

//     console.log(selected_park_name)

//     if (selected_park_name == "Select a park..") {
//         url = '/search'
//     } else {
//         url = `/search/result?park_name=${selected_park_name}`
//     }

//     console.log(url)

//     window.location.href = url
// })


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



// JS for dropdown checkbox for activities

// let options = []
// console.log(document.querySelector('.dropdown-menu a'))
// document.querySelector('.dropdown-menu a').addEventListener('click', function(event) {

//     let target = document.querySelector(event.currentTarget),
//     val = target.setAttribute('data-value'),
//     inp = target.querySelector('input'),
//     idx;

//     if ((idx = options.indexOf(val)) > -1) {
//         options.splice(idx, 1);
//         // setTimeout(function() {inp.check = false}, 0)
//     } else {
//         options.push(val)
//         // setTimeout(function() {inp.check = true}, 0)
//     }

//     document.querySelector(event.target).blur()

//     console.log(options)
//     return false
// })



// const advance_search_element = document.querySelector("#search")
// const advance_clear_element = document.querySelector("#clear")
// const park_state_element = document.querySelector(".state-name")
// const park_activities_element = document.querySelectorAll(".checkbox-activity")
// const park_topics_element = document.querySelectorAll(".checkbox-topic")

// advance_search_element.addEventListener('click', (evt) => {
//     evt.preventDefault()

//     const park_state = park_state_element.value
    
//     const park_activities = []
//     for (const activity of park_activities_element) {
//         if (activity.checked) {
//             park_activities.push(activity.innerHTML)
//         }
//     }

//     const park_topics = []
//     for (const topic in park_topics_element) {
//         if (topic.checked) {
//             park_topics.push(activity.topic)
//         }
//     }

//     const formInputs = `{state: ${park_state},
//                     activities: ${park_activities}
//                     topics: ${park_topics}}`
    
//     fetch('/new-order', {
//         method: 'POST',
//         body: JSON.stringify(formInputs),
//         headers: {
//             'Content-Type': 'application/json',
//         },
//     })
    
                    
// })
