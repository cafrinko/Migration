var map;
var results = null;

function initMap() {

    var myLatLng = {lat: -62.594, lng: -64.607};

    map = new google.maps.Map(document.getElementById('humpback-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 7,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MAPSTYLES,
        mapTypeId: 'satellite'
        // google.maps.MapTypeId.TERRAIN
    });


    $.get('/time_data.json', function (results) {

        console.log(results);
        // var positions, path;
        // var animals = animals.animals;
        // var colors = ["#FFFFFF", "#C0C0C0", "#808080", "#FF0000", "#F0A804", "#FFFF00", "#008000", "#0000FF", "#800080"];

        // for (var i=0; i<animals.length; i++) {
        //     positions = animals[i].positions;
        //     path = [];

        //     for (var j=0; j<positions.length; j++) {
        //         var lng = positions[j][0];
        //         var lat = positions[j][1];
        //         var point = new google.maps.LatLng(lat, lng);
        //         path.push(point);
        //     }
        //     // console.log(path);

        //     var polyLine = new google.maps.Polyline({
        //         path: path,
        //         map: map,
        //         strokeColor: colors[Math.floor(colors.length*Math.random())],
        //         strokeOpacity: 0.6,
        //         strokeWeight: 3,
        //         clickable: true
        //     });
        //     console.log(polyLine);

        //     polyLine.setMap(map);
        // }

        var heatmap;
        var coordinates = results.coordinates;
        // console.log(coordinates);
        function getPoints() {
            coords = [];
            // console.log(coordinates.length);
            for (var i=0; i<coordinates.length; i++) {
                console.log(i);
            // animal = animals[key];
                var point = new google.maps.LatLng(coordinates[i][0], coordinates[i][1]);
                console.log(point);
                coords.push(point);
            // console.log(coords);
            
                // for (var j=0; j<positions.length; j++) {
                //     // debugger;
                //     // console.log(positions[j]);
                //     var lng = positions[j][1];
                //     var lat = positions[j][0];
                //     var point = new google.maps.LatLng(lat, lng);
                //     coords.
                // }

            }
            return coords;
        }



        var get_points_results = getPoints();
        console.log("getPoints has been called");
        console.log(get_points_results);
        // console.log(getPoints());
        
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: get_points_results,
            map: map
        });

        heatmap.setMap(map);

        // function changeGradient() {
        //     var gradient = [
        //         'rgba(0, 255, 255, 0)',
        //         'rgba(0, 255, 255, 1)',
        //         'rgba(0, 191, 255, 1)',
        //         'rgba(0, 127, 255, 1)',
        //         'rgba(0, 63, 255, 1)',
        //         'rgba(0, 0, 255, 1)',
        //         'rgba(0, 0, 223, 1)',
        //         'rgba(0, 0, 191, 1)',
        //         'rgba(0, 0, 159, 1)',
        //         'rgba(0, 0, 127, 1)',
        //         'rgba(63, 0, 91, 1)',
        //         'rgba(127, 0, 63, 1)',
        //         'rgba(191, 0, 31, 1)',
        //         'rgba(255, 0, 0, 1)'
        //     ]
        // }

        // var positions, marker;
        // var animals = animals.animals;

        // for (var i=0; i<animals.length; i++) {
        //     // animal = animals[key];
        //     positions = animals[i].positions;

        //     for (var j=0; j<positions.length; j++) {
        //         // debugger;
        //         // console.log(positions[j]);
        //         var lng = positions[j][1];
        //         var lat = positions[j][0];
        //         marker = new google.maps.Marker({
        //             position: new google.maps.LatLng(lat, lng),
        //             map: map
        //             // title: 'Humpback ID: ' + animal + "\n coordinates: " + positions[i][0], positions[i][1]
        //         });
        //     }
        // }
    });
}

// debugger;

// google.maps.event.addDomListener(window, 'load', initMap);
