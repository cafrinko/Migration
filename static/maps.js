var map;

function initMap() {

    var myLatLng = {lat: -67.322, lng: -66.303};

    map = new google.maps.Map(document.getElementById('humpback-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 7,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MAPSTYLES,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    $.get('/data.json', function (animals) {

        var positions, path;
        var animals = animals.animals;
        var colors = ["#FFFFFF", "#C0C0C0", "#808080", "#FF0000", "#F0A804", "#FFFF00", "#008000", "#0000FF", "#800080"];

        for (var i=0; i<animals.length; i++) {
            positions = animals[i].positions;
            path = [];

            for (var j=0; j<positions.length; j++) {
                var lng = positions[j][0];
                var lat = positions[j][1];
                var point = new google.maps.LatLng(lat, lng);
                path.push(point);
            }
            // console.log(path);

            var polyLine = new google.maps.Polyline({
                path: path,
                map: map,
                strokeColor: colors[Math.floor(colors.length*Math.random())],
                strokeOpacity: 0.6,
                strokeWeight: 3,
                clickable: true
            });
            console.log(polyLine);

            polyLine.setMap(map);
        }



        // var positions, marker, html;
        // var animals = animals.animals;

        // for (var i=0; i<animals.length; i++) {
        //     // animal = animals[key];
        //     positions = animals[i].positions;

        //     for (var j=0; j<positions.length; j++) {
        //         // debugger;
        //         // console.log(positions[j]);
        //         marker = new google.maps.Marker({
                       // var lng = positions[j][1]
                       // var lat = positions[j][0];
        //             position: new google.maps.LatLng(, positions[j][0]),
        //             map: map
        //             // title: 'Humpback ID: ' + animal + "\n coordinates: " + positions[i][0], positions[i][1]
        //         });
        //     }
        // }
    });
}

// debugger;

// google.maps.event.addDomListener(window, 'load', initMap);
