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

        for (var key in animals) {
            // animal = animals[key];
            positions = animals[key];

            for (var i=0; i<=positions.length; i++) {
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(positions[i][0], positions[i][1]),
                    map: map,
                    // title: 'Humpback ID: ' + animal + "\n coordinates: " + positions[i][0], positions[i][1]
                });
            }
        }
    });
}

// google.maps.event.addDomListener(window, 'load', initMap);
