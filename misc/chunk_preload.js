async function update_map_old() {
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











async function get_rendered_chunks_idx(lat_min, lat_max, lng_min, lng_max, chunk_per_dim) {
    // get first & last chunk rendered by lat_min
    let lat_min_chunk = Math.floor((lat_min + 90) / (180 / chunk_per_dim));
    let lat_max_chunk = Math.floor((lat_max + 90) / (180 / chunk_per_dim));
    let lng_min_chunk = Math.floor((lng_min + 180) / (360 / chunk_per_dim));
    let lng_max_chunk = Math.floor((lng_max + 180) / (360 / chunk_per_dim));
    let chunk_indexes = [];
    for(let i = lat_min_chunk; i<=lat_max_chunk; i++) {
        for(let j = lng_min_chunk; j<=lng_max_chunk; j++) {
            chunk_indexes.push(i * chunk_per_dim + j);
        }
    }
    return chunk_indexes;
}

async function init_map() {

    // init map
    map = new google.maps.Map(document.getElementById('map'),  {  
        center: new google.maps.LatLng(51.505, -0.09),  
        mapTypeId: google.maps.MapTypeId.ROADMAP,  
        zoom: 11,
        disableDefaultUI: true,
    });  

    // load chunk marker array
    let chunk_per_dim = 1000;
    let lat_min = -90;
    let lat_max = 90;
    let lng_min = -180;
    let lng_max = 180;
    let markers = {};
    let rendered_chunks_indexes = new Set();
    let downloaded_markers_uids = [];
    
    // preload chunk marker arrays
    for(let i = 0; i<chunk_per_dim * chunk_per_dim; i++) { markers[i] = []; }

    async function update_map() {

        // get current map bounds
        let bounds = map.getBounds();
        let lat_min = bounds.getSouthWest().lat();
        let lng_min = bounds.getSouthWest().lng();
        let lat_max = bounds.getNorthEast().lat();
        let lng_max = bounds.getNorthEast().lng() - 0.0001; // prevent array overflow
        
        // fetch new stations
        await get_markers(lat_min, lng_min, lat_max, lng_max).then(async(data) => { 
            for(let pin of data) {
                if(pin.aqi == "-" || pin.uid in downloaded_markers_uids) continue;
                let marker = await create_marker(pin);                
                let chunk_index = Math.floor((marker.lat + 90) / (180 / chunk_per_dim)) * chunk_per_dim + Math.floor((marker.lng + 180) / (360 / chunk_per_dim));
                markers[chunk_index].push(marker);                
            }
        });

        // calculate rendered chunks
        let new_rendered_chunks = await get_rendered_chunks_idx(lat_min, lat_max, lng_min, lng_max, chunk_per_dim);
        
        for(let chunk_idx of new_rendered_chunks) {
            if(!rendered_chunks_indexes.has(chunk_idx)) {
                rendered_chunks_indexes.add(chunk_idx);
            }
        }

        // remove from rendered chunks that are not visible anymore
        for(let chunk_idx of rendered_chunks_indexes) {
            if(!new_rendered_chunks.includes(chunk_idx)) {
                rendered_chunks_indexes.delete(chunk_idx);                
                for(let marker of markers[chunk_idx]) {
                    marker.setMap(null);
                }
            }
        }

        render_zoom();

    }

    async function render_zoom() {

        let zoom = map.getZoom();
        console.log(zoom);

        // if zoom <= 7, show only the first marker of alternate chunks, hide the rest
        if(zoom <= 7) {
            for(let chunk_idx of rendered_chunks_indexes) {
                if(chunk_idx % 5 == 0 || chunk_idx % 7 == 1) {
                    if(markers[chunk_idx].length > 0) 
                        markers[chunk_idx][0].setMap(map);                    
                } else {
                    for(let marker of markers[chunk_idx]) {
                        marker.setMap(null);
                    }
                }
            }
        } 
        // if zoom > 9, show all markers for each chunk
        else {
            for(let chunk_idx of rendered_chunks_indexes) {
                for(let marker of markers[chunk_idx]) {
                    marker.setMap(map);
                }
            }
        }

    }

    // update map every dragend || 500ms
    //setInterval(update_map, 500);
    map.addListener("dragend", update_map);
    map.addListener("zoom_changed", render_zoom);

    
}

let lock = false;
async function get_markers (lat_min, lng_min, lat_max, lng_max) {
    if(lock) return [];
    lock = true;
    let url = `https://api.waqi.info/v2/map/bounds?latlng=${lat_min},${lng_min},${lat_max},${lng_max}&networks=all&token=${aqicn_api_key}`;
    let response = await fetch(url);
    let data = await response.json();
    lock = false;
    return data.data;
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
        // visible:    false,              // starting visibility

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