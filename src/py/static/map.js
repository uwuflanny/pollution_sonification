// colors are based by range
var colors = [
    '#00E400', // 0 - 50     GOOD
    '#FFFF00', // 51 - 100   MODERATE
    '#FF7E00', // 101 - 150  UNHEALTHY FOR SENSITIVE GROUPS
    '#FF0000', // 151 - 200  UNHEALTHY
    '#8F3F97', // 201 - 300  VERY UNHEALTHY
    '#000000'  // 301 - 500  HAZARDOUS
];

async function get_chunk_idx(lat, lng, chunks_per_dim) {
    let lat_chunk = Math.floor((lat + 90) / 180 * chunks_per_dim);
    let lng_chunk = Math.floor((lng + 180) / 360 * chunks_per_dim);
    return lat_chunk * chunks_per_dim + lng_chunk;
}

var map;
async function init_map() {

    // create map, add layer
    map = L.map('map').setView([51.505, -0.09], 3);
    map.doubleClickZoom.disable();
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        minZoom: 3,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // custom marker extension
    aqiMarker = L.Marker.extend({
        options: {
            aqi: 0,
            title: '',
            lat: 0,
            lng: 0
        }
    });

    // fill with circles
    await get_all_stations().then(async (data) => {
        
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
            let color_idx = Math.floor(avg_aqi / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(avg_aqi / 50);
            let color = colors[color_idx];

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

    });

    map.on('click', (event) => {
        // get click lat,lng
        let latlng = event.latlng;
        let lat = latlng.lat
        let lng = latlng.lng
        // load history
        get_today_history(lat, lng).then(async(history) => {

            // get data from history
            let aqis = await history.get_index('aqi');
            let time = await history.get_index('timestamp_local');
            
            // create graph
            create_graph(aqis, time, 'graph_plot', 'leastest AQI trend');

            // add marker
            this.marker = create_marker({
                lat: lat,
                lng: lng,
                aqi: aqis[aqis.length - 1], // get last element
            });
            
        });  
    });

}

async function create_marker (pin) {
    
    let lat = pin.lat;
    let lng = pin.lng;
    let aqi = pin.aqi;

    // get color idx and text color
    let color_idx = Math.floor(aqi / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(aqi / 50);
    let text_color = (parseInt(colors[color_idx].replace('#', ''), 16) > 0xffffff / 2) ? '#000' : '#fff';      

    // create leaflet marker
    return marker = new aqiMarker([lat, lng], {

        // custom marker label
        icon: L.divIcon({
            className: 'my-div-icon',
            html:
                `<img class="my-div-image" src="./static/img/${color_idx}-sign.png"/>
                <span class="my-div-span" style="background-color: ${colors[color_idx]}; color: ${text_color}">${aqi}</span>`,
        }),

        // additional marker info
        aqi: aqi,
        title: `TEST`,
        lat: lat,
        lng: lng,
        
    }).addTo(map).on('click', show_offcanvas);
    
}
