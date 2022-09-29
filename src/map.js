// colors are based by range
var aqicn_api_key = 'd7997a4e2fa35a67576fa7e7e766f6f226cf59f5';
var colors = [
    '#00E400', // 0 - 50     GOOD
    '#FFFF00', // 51 - 100   MODERATE
    '#FF7E00', // 101 - 150  UNHEALTHY FOR SENSITIVE GROUPS
    '#FF0000', // 151 - 200  UNHEALTHY
    '#8F3F97', // 201 - 300  VERY UNHEALTHY
    '#000000'  // 301 - 500  HAZARDOUS
];

async function get_all_stations() {
    let url = `https://api.waqi.info/v2/map/bounds?latlng=-90,-180,90,180&networks=all&token=${aqicn_api_key}`;
    let response = await fetch(url);
    let data = await response.json();
    return data.data;
}


async function get_chunk_idx(lat, lng, chunks_per_dim) {
    let lat_chunk = Math.floor((lat + 90) / 180 * chunks_per_dim);
    let lng_chunk = Math.floor((lng + 180) / 360 * chunks_per_dim);
    return lat_chunk * chunks_per_dim + lng_chunk;
}


var map;
async function init_map() {

    // init map
    map = new google.maps.Map(document.getElementById('map'),  {  
        center: new google.maps.LatLng(51.505, -0.09),  
        mapTypeId: google.maps.MapTypeId.ROADMAP,  
        zoom: 3,
        disableDefaultUI: true,
        disableDoubleClickZoom: true,        
        minZoom: 3
    });  


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
            new google.maps.Circle({
                strokeColor: color,
                strokeOpacity: 0.4,
                strokeWeight: 2,
                fillColor: color,
                fillOpacity: 0.075,
                map: map,
                center: {lat: avg_lat, lng: avg_lng},
                radius: size * 50000,
                clickable: false
            });

        }

    });


    // on map click
    map.addListener('click', (mouse) => {
        // remove old marker
        if(typeof this.marker != 'undefined') this.marker.setMap(null);
        // get click lat lang
        let lat = mouse.latLng.lat();
        let lng = mouse.latLng.lng();
        // load history
        get_today_history(lat, lng).then((history) => {
            // create graph
            create_graph(history, 'aqi', 'graph_plot', 'leastest AQI trend');
            // add marker
            create_marker({
                lat: lat,
                lng: lng,
                aqi: 69,    // TODO get aqi from history
            }).then((marker) => {
                this.marker = marker;
            });
        });                            
    });

}


async function set_marker_appearance(marker) {
    // TODO set color, image, label here ...
}

async function create_marker (pin) {
    
    let lat = pin.lat;
    let lng = pin.lng;
    let aqi = pin.aqi;

    // get color idx and text color
    let color_idx = Math.floor(aqi / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(aqi / 50);
    let text_color = (parseInt(colors[color_idx].replace('#', ''), 16) > 0xffffff / 2) ? '#000' : '#fff';      
    let pos = new google.maps.LatLng(lat, lng);

    let marker = new google.maps.Marker({

        position:   pos,    // marker position (lat & lng)
        map:        map,    // map to add marker to
        aqi:        aqi,    // aqi value
        lat:        lat,    // lat
        lng:        lng,    // lng

        // custom marker label
        label: {
            text: String(aqi),
            color: text_color,
            fontSize: "16px",
            fontWeight: "bold"
        },

        // custom marker icon
        icon: {
            url: `./img/${color_idx}-sign.png`
        }

    });

    marker.addListener('click', marker_click);
    return marker;
}

async function marker_click () {
    let myOffcanvas = document.getElementById('sonificate');
    new bootstrap.Offcanvas(myOffcanvas).show();    
    // fill offcanvas
    $("#sonificate_p").attr("data-lat", this.lat);
    $("#sonificate_p").attr("data-lng", this.lng);
    $("#sonificate_title").text(this.title);
    $("#sonificate_p").text(this.aqi);
    $("#startDate").val("");
    $("#endDate").val("");
}
