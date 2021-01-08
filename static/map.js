PARIS_COORD = [48.864, 2.349];

var mymap = L.map('mapid').setView(PARIS_COORD, 7);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
}).addTo(mymap);

var sources = [ new EventSource('/ISS'),
                                new EventSource('/NOAA_19') ];

ISS_marker = [];
sources[0].addEventListener('message', function(e){
        console.log('Message');
        obj = JSON.parse(e.data);
        console.log(obj);

        console.log(ISS_marker.length)
        for (var i = 0; i < ISS_marker.length; i++){
                mymap.removeLayer(ISS_marker[i]);
        }

        marker = L.marker([obj.latitude, obj.longitude])
                         .bindTooltip('ISS', { noHide: true })
                         .addTo(mymap);
        ISS_marker.push(marker);
}, false);

NOAA_19_marker = [];
sources[1].addEventListener('message', function(e){
        console.log('Message');
        obj = JSON.parse(e.data);
        console.log(obj);

        for (var i = 0; i < NOAA_19_marker.length; i++){
                mymap.removeLayer(NOAA_19_marker[i]);
        }

        marker = L.marker([obj.latitude, obj.longitude])
                         .bindTooltip('NOAA 19', { noHide: true })
                         .addTo(mymap);
        NOAA_19_marker.push(marker);
}, false);

var circle = L.circle(PARIS_COORD, {
color: 'red',
fillColor: '#f03',
fillOpacity: 0.5,
radius: 500000
}).addTo(mymap);

