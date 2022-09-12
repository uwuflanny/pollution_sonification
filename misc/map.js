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
    lng -= 0.0001;
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
                fillOpacity: 0.1,
                map: map,
                center: {lat: avg_lat, lng: avg_lng},
                radius: size * 50000,
                clickable: false
            });

        }

    });


    // on map click
    map.addListener('click', (mouse) => {
        // get click lat lang
        let lat = mouse.latLng.lat();
        let lng = mouse.latLng.lng();
        // get aqi
        let url = `https://api.waqi.info/feed/geo:${lat};${lng}/?token=${aqicn_api_key}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                let pin = data.data;
                create_marker(pin);
                // move map to pin location with animation
                map.panTo(new google.maps.LatLng(pin.city.geo[0], pin.city.geo[1]));
            });
    });

}


async function set_marker_appearance(marker) {
    // TODO set color, image, label here ...
}

async function create_marker (pin) {
    
    // get color idx and text color
    let color_idx = Math.floor(pin.aqi / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(pin.aqi / 50);
    let text_color = (parseInt(colors[color_idx].replace('#', ''), 16) > 0xffffff / 2) ? '#000' : '#fff';      
    let pos = new google.maps.LatLng(pin.city.geo[0], pin.city.geo[1]);

    let marker = new google.maps.Marker({

        position:   pos,                // marker position (lat & lng)
        map:        map,                // map to add marker to
        title:      pin.city.name,   // marker title
        aqi:        pin.aqi,            // aqi value
        lat:        pin.city.geo[0],            // lat
        lng:        pin.city.geo[1],            // lng

        // custom marker label
        label: {
            text: pin.aqi.toString(),
            color: text_color,
            fontSize: "16px",
            fontWeight: "bold"
        },

        // custom marker icon
        icon: {
            url: `./img/${color_idx}-sign.png`
        }                    

    });

    let contentString = 
        `<div style="background-color: ${colors[color_idx]};">
            <p>${pin.city.name} ${pin.aqi}</p>                        
        </div>`;

    let info_window = new google.maps.InfoWindow({
        content: contentString,
        disableAutoPan: true,
    });

    // mouse events
    marker.addListener('click',     marker_click);
    marker.addListener('mouseout',  () => { info_window.close(); });
    marker.addListener('mouseover', () => {
        info_window.open({
            anchor: marker,
            map,
            shouldFocus: true,
        });
    });

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
