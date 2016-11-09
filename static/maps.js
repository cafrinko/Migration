var map;

function initMap() {

    var myLatLng = {lat: -70, lng: -70};

    map = new google.maps.Map(document.getElementById('humpback-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 5,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MAPSTYLES,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    $.get('/data.json', function (animals) {

        var positions, marker, html;
        var animals = animals.animals;

        for (var i=0; i<animals.length; i++) {
            // animal = animals[key];
            positions = animals[i].positions;

            for (var j=0; j<positions.length; j++) {
                // debugger;
                // console.log(positions[j]);
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(positions[j][0], positions[j][1]),
                    map: map
                    // title: 'Humpback ID: ' + animal + "\n coordinates: " + positions[i][0], positions[i][1]
                });
            }
        }
    });
}

// debugger;

// google.maps.event.addDomListener(window, 'load', initMap);
