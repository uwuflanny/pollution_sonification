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

// lat -90  to 90
// lng -180 to 180
var marker_clusters = {};
var MERIDIANS = 24;
var PARALLELS = 12;
function get_marker_grid_position(lat, lng) {
    let meridian = Math.floor((lng + 180) / 360 * MERIDIANS);
    let parallel = Math.floor((lat + 90) / 180 * PARALLELS);
    return meridian * MERIDIANS + parallel;
}

var markers = {};
var map;
async function init_map() {

    // init map
    map = new google.maps.Map(document.getElementById('map'),  {  
        center:  new  google.maps.LatLng(51.505,  -0.09),  
        mapTypeId:  google.maps.MapTypeId.ROADMAP,  
        zoom:  11,
        disableDefaultUI: true,
    });  

    // init clusters
    for (let i = 0; i < MERIDIANS; i++) {
        for (let j = 0; j < PARALLELS; j++) {
            let idx = i * MERIDIANS + j;
            marker_clusters[idx] = new MarkerClusterer(map, []);
        }        
    }

    // custom marker on double click
    map.addListener('dblclick', async (e) => {
        // get lat, lang, location name
        let lat = e.latLng.lat();
        let lng = e.latLng.lng();
        let url = `https://api.waqi.info/feed/geo:${lat};${lng}/?token=${aqicn_api_key}`;
        let response = await fetch(url);
        let data = await response.json();
        let pin = data.data;
        marker_click.call({
            lat: lat,
            lng: lng,
            title: "custom marker",
            aqi: pin.aqi,
        });
    });

    // TODO PERIODICALLY UPDATE MARKERS
    map.addListener("bounds_changed", async function() {

        // get lat lng bounds
        let bounds = map.getBounds();
        let lat_min = bounds.getSouthWest().lat();
        let lat_max = bounds.getNorthEast().lat();
        let lng_min = bounds.getSouthWest().lng();
        let lng_max = bounds.getNorthEast().lng();
    
        // TODO PERIODICALLY UPDATE RENDERED MARKERS
        await get_markers(lat_min, lng_min, lat_max, lng_max).then(data => {            
    
            for(let pin of data) {                
                if (pin.aqi == null || pin.aqi == '-' || pin.uid in markers)  continue;                
                markers[pin.uid] = create_marker(pin);              
            }
    
        });
    
    });
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

        // custom marker label
        label: {
            text: pin.aqi.toString(),
            color: text_color,
            fontSize: "16px",
            fontWeight: "bold"
        },

        // custom marker icon
        icon: {
            url: `./img/${color_idx}-sign.png`,
            scaledSize: new google.maps.Size(50, 50)
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

    let grid_pos = get_marker_grid_position(pin.lat, pin.lon);


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
