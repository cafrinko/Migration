var map1, map2;
var results = null;

function initMap() {

    var polylineMapLatLng = {lat: -64, lng: -62};

    map1 = new google.maps.Map(document.getElementById('polyline-map'), {
        center: polylineMapLatLng,
        scrollwheel: false,
        zoom: 5,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MARKERMAP,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    var heatmapLatLng = {lat: -62.594, lng: -64.607};

    map2 = new google.maps.Map(document.getElementById('heatmap'), {
        center: heatmapLatLng,
        scrollwheel: false,
        zoom: 7,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: HEATMAP,
        mapTypeId: 'satellite'
        // google.maps.MapTypeId.TERRAIN
    });

    $.get('/animal_data.json', function (animals) {

        var positions, paths;
        var animals = animals.animals;
        var colors = ["#FFFFFF", "#C0C0C0", "#808080", "#FF0000", "#F0A804", "#FFFF00", "#008000", "#0000FF", "#800080"];

        for (var i=0; i<animals.length; i++) {
            positions = animals[i].positions;
            paths = [];

            for (var j=0; j<positions.length; j++) {
                var lng = positions[j][0];
                var lat = positions[j][1];
                var point = new google.maps.LatLng(lat, lng);
                paths.push(point);
            }
            console.log(paths);

            var polyLine = new google.maps.Polyline({
                path: paths,
                map: map1,
                strokeColor: colors[Math.floor(colors.length*Math.random())],
                strokeOpacity: 0.6,
                strokeWeight: 3,
                clickable: true
            });
            // console.log(polyLine);

            polyLine.setMap(map1);

            var blah = animals[i].animal[0][0].toString();

            var url = '/animal_id/' + blah

            // google.maps.event.addListener(polyLine, 'click', function() {
            //     $.get(url);
            // });
        }
    });

    $.get('/time_data.json?year=2016&month=04&day=30', updateMap);

    function updateMap (results) {

        var heatmap;
        var coordinates = results.coordinates;
        function getPoints() {
            coords = [];
            // console.log(coordinates.length);
            for (var i=0; i<coordinates.length; i++) {
                console.log(i);
                var point = new google.maps.LatLng(coordinates[i][0], coordinates[i][1]);
                console.log(point);
                coords.push(point);
            }
            return coords;
        }

        var get_points_results = getPoints();
        console.log("getPoints has been called");
        console.log(get_points_results);
        // console.log(getPoints());
        
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: get_points_results,
            map: map2
        });

        heatmap.setMap(map2);
    }

    $('#heatmap-form').on('submit', function (evt) {
        console.log("hey");
        evt.preventDefault();
        $.get('/time_data.json', { year: "2016", month: "05", day: "05"}, updateMap);
    });
}

// google.maps.event.addDomListener(window, 'load', initMap);