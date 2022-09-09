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



async function divide_in_chunks() {
    
    // queries should be done in chunksize = 5x5, map in 30x30

    let chunk_per_dim_query = 5;
    let chunk_per_dim_map = 30;
    let chunk_ratio = chunk_per_dim_map / chunk_per_dim_query;
    let lat_min = -90;
    let lat_max = 90;
    let lng_min = -180;
    let lng_max = 180;

    let markers = {};

    for(let i = 0; i < chunk_per_dim_query; i++) {
        for(let j = 0; j < chunk_per_dim_query; j++) {

            // calc start and end lat lng
            let lat_start = lat_min + (lat_max - lat_min) * i / chunk_per_dim_query;
            let lat_end =   lat_min + (lat_max - lat_min) * (i + 1) / chunk_per_dim_query;
            let lng_start = lng_min + (lng_max - lng_min) * j / chunk_per_dim_query;
            let lng_end =   lng_min + (lng_max - lng_min) * (j + 1) / chunk_per_dim_query;

            // create sub chunks arrays
            for(let k = 0; k < chunk_ratio; k++) {
                for(let l = 0; l < chunk_ratio; l++) {
                    // get index of sub chunk incremental
                    let index = ((i * chunk_per_dim_query) + j) * (chunk_ratio * chunk_ratio) + (k * chunk_ratio) + l;
                    markers[index] = [];
                }
            }

            // get stations
            let url = `https://api.waqi.info/map/bounds/?latlng=${lat_start},${lng_start},${lat_end},${lng_end}&token=${aqicn_api_key}`;
            let response = await fetch(url);
            let data = await response.json();
            let stations = data.data;

            // TODO FIX
            function calc_subchunk_index(lat, lng) {
                let lat_index = Math.floor((lat - lat_start) / (lat_end - lat_start) * chunk_ratio);
                let lng_index = Math.floor((lng - lng_start) / (lng_end - lng_start) * chunk_ratio);
                let idx = lat_index * chunk_ratio + lng_index
                console.log(idx);
                return idx;
            }            
            
            // create markers
            for(let pin of stations) {
                if (pin.aqi == null || pin.aqi == '-') continue;
                let marker = await create_marker(pin);
                markers[calc_subchunk_index(marker.lat, marker.lng)].push(marker);
            }

            //console.log(i,j);

        }
    }

    return markers;
    
}


async function get_all_stations() {
    let url = `https://api.waqi.info/v2/map/bounds?latlng=-90,-180,90,180&networks=all&token=${aqicn_api_key}`;
    let response = await fetch(url);
    let data = await response.json();
    return data.data;
}


var map;
async function init_map() {

    divide_in_chunks();

    // init map
    map = new google.maps.Map(document.getElementById('map'),  {  
        center: new google.maps.LatLng(51.505, -0.09),  
        mapTypeId: google.maps.MapTypeId.ROADMAP,  
        zoom: 11,
        disableDefaultUI: true,
    });  


    let markers = {};
    async function update_map() {


        let bounds = map.getBounds();
        let lat_min = bounds.getSouthWest().lat();
        let lng_min = bounds.getSouthWest().lng();
        let lat_max = bounds.getNorthEast().lat();
        let lng_max = bounds.getNorthEast().lng();

        // if map is 30x30 chunks, print chunk id that should be rendered
        let chunk_per_dim = 30;
        let chunk_size = (lat_max - lat_min) / chunk_per_dim;



        /*

        // get lat lng bounds
        let bounds = map.getBounds();
        let lat_min = bounds.getSouthWest().lat();
        let lat_max = bounds.getNorthEast().lat();
        let lng_min = bounds.getSouthWest().lng();
        let lng_max = bounds.getNorthEast().lng();

        // render new markers
        await get_markers(lat_min, lng_min, lat_max, lng_max).then(async(data) => {            

            for(let pin of data) {                

                if (pin.aqi == null || pin.aqi == '-' || pin.uid in markers) continue;
                let marker = await create_marker(pin);
                markers[pin.uid] = marker;

            }

        });

        // TODO DIVIDE MAP IN CHUNKS
        // PRELOAD ALL CHUNKS AS INVISIBLE MARKERS
        // WHEN MAP IS MOVED, GET RENDERED CHUNKS
        // CHECK HOW MANY STATIONS ARE RENDERED, DO NOT RENDER OTHERS

        // set invisible to all markers   
        for(let uid in markers) {
            let marker = markers[uid];
            let lat = marker.lat;
            let lng = marker.lng;
            marker.setVisible(lat >= lat_min && lat <= lat_max && lng >= lng_min && lng <= lng_max);
        }

        */

    }

    // update map every dragend || 500ms
    //setInterval(update_map, 500);
    map.addListener("dragend", update_map);
    map.addListener("zoom_changed", update_map);

    
}

var lock = false;
async function get_markers (lat_min, lng_min, lat_max, lng_max) {
    if (lock) return [];
    lock = true;
    let url = `https://api.waqi.info/v2/map/bounds?latlng=${lat_min},${lng_min},${lat_max},${lng_max}&networks=all&token=${aqicn_api_key}`;
    let response = await fetch(url);
    let data = await response.json();
    lock = false;
    return data.data;
}

async function set_marker_appearance(marker) {
    // TODO set color, image, label here ...
}

async function create_marker (pin) {
    
    // get color idx and text color
    let color_idx = Math.floor(pin.aqi / 50) > colors.length - 1 ? colors.length - 1 : Math.floor(pin.aqi / 50);
    let text_color = (parseInt(colors[color_idx].replace('#', ''), 16) > 0xffffff / 2) ? '#000' : '#fff';      
    let pos = new google.maps.LatLng(pin.lat, pin.lon);

    let marker = new google.maps.Marker({

        position:   pos,                // marker position (lat & lng)
        map:        map,                // map to add marker to
        title:      pin.station.name,   // marker title
        uid:        pin.uid,            // unique id (station id)
        aqi:        pin.aqi,            // aqi value
        lat:        pin.lat,            // lat
        lng:        pin.lon,            // lng
        visible:    false,              // visible

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
            <p>${pin.station.name} ${pin.aqi} ${pin.uid}</p>                        
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
