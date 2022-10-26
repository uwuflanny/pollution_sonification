
// colors are based by range
var colors = [
    '#00E400', // 0 - 50     GOOD
    '#FFFF00', // 51 - 100   MODERATE
    '#FF7E00', // 101 - 150  UNHEALTHY FOR SENSITIVE GROUPS
    '#FF0000', // 151 - 200  UNHEALTHY
    '#8F3F97', // 201 - 300  VERY UNHEALTHY
    '#000000'  // 301 - 500  HAZARDOUS
];

var emojis = [
    "😍",
    "😃",
    "😶",
    "🙁",
    "😰",
    "💀"
];

// get color id, text color
function get_color_idx(aqi) {
    if (aqi <= 50) return 0;
    else if (aqi <= 100) return 1;
    else if (aqi <= 150) return 2;
    else if (aqi <= 200) return 3;
    else if (aqi <= 300) return 4;
    else return 5;
}
function get_color(aqi) {
    return colors[get_color_idx(aqi)];
}
function get_emoji(aqi) {
    return emojis[get_color_idx(aqi)];
}
function get_text_color(aqi){
    let color = get_color(aqi);
    let r = parseInt(color.substring(1, 3), 16);
    let g = parseInt(color.substring(3, 5), 16);
    let b = parseInt(color.substring(5, 7), 16);
    let brightness = (r * 299 + g * 587 + b * 114) / 1000;
    return brightness > 125 ? 'black' : 'white';
}


// loads circles on map. data: all stations data
async function load_circles(data) {

    // get chunk unique index
    async function get_chunk_idx(lat, lng, chunks_per_dim) {
        let lat_chunk = Math.floor((lat + 90) / 180 * chunks_per_dim);
        let lng_chunk = Math.floor((lng + 180) / 360 * chunks_per_dim);
        return lat_chunk * chunks_per_dim + lng_chunk;
    }

    // create chunks
    let chunks = {};
    let chunks_per_dim = 70;   
    for (let i = 0; i < chunks_per_dim * chunks_per_dim; i++) chunks[i] = [];

    // load chunks
    for(let pin of data) {
        if(pin.aqi == '-') continue;
        let lat = pin.lat;
        let lng = pin.lon;
        let chunk_idx = await get_chunk_idx(lat, lng, chunks_per_dim);
        chunks[chunk_idx].push(pin);
    }

    // for each chunk, calculate avg aqi, lat & lng -> then draw circle
    for (let i = 0; i < chunks_per_dim * chunks_per_dim; i++) {

        // skip empty chunks
        let chunk = chunks[i];
        let size = chunk.length;
        if (size == 0) continue;

        // calculate average aqi, lat, and lng
        let avg_aqi = chunk.reduce((a, b) => a + Number(b.aqi), 0) / size;
        let avg_lat = chunk.reduce((a, b) => a + Number(b.lat), 0) / size;
        let avg_lng = chunk.reduce((a, b) => a + Number(b.lon), 0) / size;
        
        // get color
        let color = get_color(avg_aqi);

        // draw circle shape
        L.circle([avg_lat, avg_lng], {
            color: color,
            fillColor: color,
            opacity: 0.6,
            fillOpacity: 0.15,
            radius: size * 40000,
            clickable: false,
        }).addTo(map);

    }

}

async function init_map() {

    // load map and layout
    map = L.map('map').setView([15, 21], 3);
    map.doubleClickZoom.disable();
    document.querySelector('.leaflet-bottom.leaflet-right').remove();
    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
        maxZoom: 18,
        minZoom: 3,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' + ' <a href='
        + '"https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © ' + '<a href="http://stadiamaps.com">Stadia Maps</a>, '
        + '<a href="https://openmaptiles.org/">OpenMapTiles</a> &mdash; Map tiles by <a href="https://stadiamaps.com/">Stadia Maps</a>, ' +
        '<a href="https://openmaptiles.org/">OpenMapTiles</a> &mdash; ' +
        'Data by <a href="http://openweathermap.org">OpenWeatherMap</a>, <a href="http://aqicn.org">AQICN</a>',
    }).addTo(map);

    // custom marker extension
    aqiMarker = L.Marker.extend({
        options: {
            aqi: 0,
            location: '',
            lat: 0,
            lng: 0
        }
    });
    
    // geocoder
    var searchControl = L.esri.Geocoding.geosearch({
        placeholder: 'Enter an address or place e.g. 1 York St',
        useMapBounds: false,
        providers: [L.esri.Geocoding.arcgisOnlineProvider({apikey: "AAPK150e6843de69411582a2fb7010285854YRNW0bRLWXXr9R5W35IlgRQAuGpVWg3jVIXeg1vOm3SUViRtqj5AeCNpe-qMQXS4", nearby: {lat: -33.8688, lng: 151.2093}})]
    }).addTo(map);

    // geocoder action
    var results = L.layerGroup().addTo(map);
    searchControl.on('results', function(data){
        results.clearLayers();
        for (var i = data.results.length - 1; i >= 0; i--) {
            map_inspect(data.results[i]);
        }
    });

    // reverse geocode
    geocodeService = L.esri.Geocoding.geocodeService({
        apikey: "AAPK150e6843de69411582a2fb7010285854YRNW0bRLWXXr9R5W35IlgRQAuGpVWg3jVIXeg1vOm3SUViRtqj5AeCNpe-qMQXS4"
    });

    // actions
    map.on('click', map_inspect);
    await get_all_stations().then(load_circles);

}


// map click action: plot aqi, create marker on click location
async function map_inspect(event) {

    // get click lat,lng
    let latlng = event.latlng;
    let lat = latlng.lat
    let lng = latlng.lng
    
    await geocodeService.reverse().latlng(event.latlng).run(async function (error, result) {

        // get address
        let add = result.address;
        let location = add.City || add.LongLabel;

        // add marker
        create_marker(lat, lng, location);

    });

}


// marker click action: show offcanvas
async function create_marker(lat, lng, location) {
    
    // load history
    get_today_history(lat, lng).then(async(history) => {

        let id = String(Date.now());
        let aqis = await history.get_index('aqi');
        let time = await history.get_index('timestamp_local');
        let aqi = aqis[aqis.length - 1];

        new aqiMarker([lat, lng], {

            // custom marker label
            icon: L.divIcon({
                className: 'my-div-icon',
                html:
                    `<div class="speech-bubble">
                        ${location} AQI: ${aqi} ${get_emoji(aqi)}
                        <img class="aqi_preview" id="${id}"></img>
                    </div>`,
            }),
    
            // additional marker info
            location: location,
            aqi: aqi,
            lat: lat,
            lng: lng,
    
        }).addTo(map).on('click', load_offcanvas).on('contextmenu', function(e) { map.removeLayer(this); });
    
        create_small_graph(aqis, time, id);

    });
    
}
