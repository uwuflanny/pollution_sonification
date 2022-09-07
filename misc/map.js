// colors are based by range
var colors = [
    '#00E400', // 0 - 50     GOOD
    '#FFFF00', // 51 - 100   MODERATE
    '#FF7E00', // 101 - 150  UNHEALTHY FOR SENSITIVE GROUPS
    '#FF0000', // 151 - 200  UNHEALTHY
    '#8F3F97', // 201 - 300  VERY UNHEALTHY
    '#7E0023'  // 301 - 500  HAZARDOUS
];

var markers = {};
var map;
async function init_map() {
    map = new google.maps.Map(document.getElementById('map'),  {  
        center:  new  google.maps.LatLng(51.505,  -0.09),  
        mapTypeId:  google.maps.MapTypeId.ROADMAP,  
        zoom:  11  
    });  

    // TODO PERIODICALLY UPDATE MARKERS
    map.addListener("bounds_changed", async function() {

        // get lat lng bounds
        let bounds = map.getBounds();
        let lat_min = bounds.getSouthWest().lat();
        let lat_max = bounds.getNorthEast().lat();
        let lng_min = bounds.getSouthWest().lng();
        let lng_max = bounds.getNorthEast().lng();
    
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
    let url = `https://api.waqi.info/v2/map/bounds?latlng=${lat_min},${lng_min},${lat_max},${lng_max}&networks=all&token=d7997a4e2fa35a67576fa7e7e766f6f226cf59f5`;
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

        // custom marker label
        label: {
            text: pin.aqi.toString(),
            color: text_color,
            fontSize: "18px",
            fontWeight: "bold"
        },

        // custom marker icon
        icon: {
            url: `./img/${color_idx}-sign.png`,
            scaledSize: new google.maps.Size(30, 30)
        }                    

    });

    let contentString = 
        `<div>
            <p>${pin.station.name}</p>                        
            <p style="background-color: ${colors[color_idx]};">${pin.aqi}</p>                        
        </div>`;

    let info_window = new google.maps.InfoWindow({
        content: contentString,
        disableAutoPan: true
    });
    marker.addListener('mouseover', function() {
        info_window.open({
            anchor: marker,
            map,
            shouldFocus: true,
        });
    });
    marker.addListener('mouseout', function() {                    
        info_window.close();                
    });

    return marker;
}
