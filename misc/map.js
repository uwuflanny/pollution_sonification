// colors are based by range
var aqicn_api_key = 'd7997a4e2fa35a67576fa7e7e766f6f226cf59f5';
var colors = [
    '#00E400', // 0 - 50     GOOD
    '#FFFF00', // 51 - 100   MODERATE
    '#FF7E00', // 101 - 150  UNHEALTHY FOR SENSITIVE GROUPS
    '#FF0000', // 151 - 200  UNHEALTHY
    '#8F3F97', // 201 - 300  VERY UNHEALTHY
    '#FFFFFF'  // 301 - 500  HAZARDOUS
];

async function get_all_stations() {
    let url = `https://api.waqi.info/v2/map/bounds?latlng=-90,-180,90,180&networks=all&token=${aqicn_api_key}`;
    let response = await fetch(url);
    let data = await response.json();
    return data.data;
}



async function get_all_stations(){
    let url = `https://api.waqi.info/v2/map/bounds?latlng=-90,-180,90,180&networks=all&token=${aqicn_api_key}`;
    let response = await fetch(url);
    let data = await response.json();
    return data.data;
}


var map;
async function init_map() {

    // init map
    map = new google.maps.Map(document.getElementById('map'),  {  
        center: new google.maps.LatLng(51.505, -0.09),  
        mapTypeId: google.maps.MapTypeId.ROADMAP,  
        zoom: 11,
        disableDefaultUI: true,
    });  


    let chunks_per_dim = 100;
    async function get_chunk_idx(lat,lng) {
        let lat_chunk = Math.floor((lat + 90) / 180 * chunks_per_dim);
        let lng_chunk = Math.floor((lng + 180) / 360 * chunks_per_dim);
        return lat_chunk * chunks_per_dim + lng_chunk;
    }
    await get_all_stations().then(async (data) => {
        // divide data into chunks
        // assign each chunk a size based on number of stations and a color based on avg aqi

        // create chunks
        let chunks = {};
        for (let i = 0; i < chunks_per_dim * chunks_per_dim; i++) { chunks[i] = []; }

        // load chunks
        for(let pin of data) {
            let lat = pin.lat;
            let lng = pin.lon;
            let aqi = pin.aqi;
            let chunk_idx = await get_chunk_idx(lat,lng);
            chunks[chunk_idx].push(aqi);
        }

        // for each chunk, calculate avg aqi and size
        let chunk_sizes = {};
        let chunk_avg_aqis = {};
        let chunk_locations = {};
        for (let i = 0; i < chunks_per_dim * chunks_per_dim; i++) {
            let chunk = chunks[i];
            let size = chunk.length;
            let avg_aqi = chunk.reduce((a, b) => a + b, 0) / size;

            // set location to the nearest point to all the points in the chunk
            let lat = 0;
            let lng = 0;
            for (let p of chunk) {
                lat += p.lat;
                lng += p.lng;
            }
            lat /= size;
            lng /= size;

            chunk_locations [i] = {lat: lat, lng: lng};
            chunk_sizes[i] = size;
            chunk_avg_aqis[i] = avg_aqi;
        }

        for(let i = 0; i < chunks_per_dim; i++) {
            for(let j = 0; j < chunks_per_dim; j++) {

                let idx = i * chunks_per_dim + j;

                let color_idx = Math.floor(chunk_avg_aqis[idx] / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(chunk_avg_aqis[idx] / 50);
                let color = colors[color_idx];

                // draw circle shape
                let circle = new google.maps.Circle({
                    strokeColor: color,
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: color,
                    fillOpacity: 0.35,
                    map: map,
                    center: chunk_locations[idx],
                    radius: Math.sqrt(chunk_sizes[idx]) * 100000
                });

            }
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
