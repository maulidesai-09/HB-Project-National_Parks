// JS for Google Maps to be displayed on Park Details page

function initMap() {

    const parkLat = parseFloat(document.querySelector("#lat").innerHTML)
    const parkLong = parseFloat(document.querySelector("#long").innerHTML)
    const parkName = document.querySelector("#park_name").innerHTML

    const parkCoords = {
                        lat: parkLat, 
                        lng: parkLong};

    console.log(parkCoords)

    const parkInfo = `
    <h1> ${parkName} </h1>
    <p>
    Located at: <code> ${parkLat} </code>
                <code> ${parkLong} </code>
    </p>`

    
    const basicMap = new google.maps.Map(document.querySelector("#map"), {
        center: parkCoords,
        zoom: 4.5
    }
    );

    const parkMarker = new google.maps.Marker({
        position: parkCoords,
        title: parkName,
        map: basicMap
    });

    const InfoWindow = new google.maps.InfoWindow({
        content: parkInfo,
        maxWidth: 200
    });

    parkMarker.addListener('click', () => {
        InfoWindow.open(basicMap, parkMarker);
    });

}