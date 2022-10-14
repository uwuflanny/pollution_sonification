
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
    return Math.floor(aqi / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(aqi / 50);
}
function get_text_color(aqi) {
    return (parseInt(colors[get_color_idx(aqi)].replace('#', ''), 16) > 0xffffff / 2) ? '#000' : '#f0f0f0'
}
function get_color(aqi) {
    return colors[get_color_idx(aqi)];
}
function get_emoji(aqi) {
    return emojis[get_color_idx(aqi)];
}
function get_sign_image(aqi) {
    return `./static/img/${get_color_idx(aqi)}-sign.png`;
}


// get chunk unique index
async function get_chunk_idx(lat, lng, chunks_per_dim) {
    let lat_chunk = Math.floor((lat + 90) / 180 * chunks_per_dim);
    let lng_chunk = Math.floor((lng + 180) / 360 * chunks_per_dim);
    return lat_chunk * chunks_per_dim + lng_chunk;
}


// loads circles on map. data: all stations data
async function load_circles(data) {

    // create chunks
    let chunks = {};
    let chunks_per_dim = 70;   
    for (let i = 0; i < chunks_per_dim * chunks_per_dim; i++) { chunks[i] = []; }

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

        // basic chunk info
        let chunk = chunks[i];
        let size = chunk.length;
        if (size == 0) continue;

        // calculate average aqi, lat, and lng
        let avg_aqi = chunk.reduce((a, b) => a + Number(b.aqi), 0) / size;
        let avg_lat = chunk.reduce((a, b) => a + Number(b.lat), 0) / size;
        let avg_lng = chunk.reduce((a, b) => a + Number(b.lon), 0) / size;
        
        // calculate color
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

    // create map, add layer
    map = L.map('map').setView([51.505, -0.09], screen.width <= 500 ? 6 : 3);
    map.zoomControl.remove();
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

    // load history
    get_today_history(lat, lng).then(async(history) => {

        // plot graph
        let aqis = await history.get_index('aqi');
        let time = await history.get_index('timestamp_local');
        create_graph_image(aqis, time, 'graph_plot', 'leastest AQI trend');

        // add marker
        this.marker = create_marker({
            lat: lat,
            lng: lng,
            aqi: aqis[aqis.length - 1], // get last element
        });
        
    }); 

}


// marker click action: show offcanvas
async function create_marker (pin) {
    
    // get coords
    let lat = pin.lat;
    let lng = pin.lng;
    let aqi = pin.aqi;

    // get color idx and text color
    let image = get_sign_image(aqi);
    let color = get_color(aqi);
    let text_color = get_text_color(aqi);      

    // create leaflet marker
    return marker = new aqiMarker([lat, lng], {

        // custom marker label
        icon: L.divIcon({
            className: 'my-div-icon',
            html:
                `<div style="position:relative;">
                    <span class="sign" style="color: ${text_color}; background-color:${color};">${aqi}</span>
                </div>`,
                
        }),

        // additional marker info
        location: `location here`,
        aqi: aqi,
        lat: lat,
        lng: lng,
        
    }).addTo(map).on('click', show_offcanvas);
    
}
