
function AqiManager(weatherbit_key = 'c0756c0b51cd4bdb9e98c7582b3dfc06') {
    this.key = weatherbit_key;
}

// add prototype load to aqimamager
AqiManager.prototype.load = async function(lat, lng, start_date, end_date) {
    if(this.lat == lat && this.lng == lng) return;
    this.lat = lat;
    this.lng = lng;
    let request = `https://api.weatherbit.io/v2.0/history/airquality?lat=${lat}&lon=${lng}&start_date=${start_date}&end_date=${end_date}&tz=local&key=${this.key}`;
    let response = await fetch(request);
    this.data = await response.json();
}

AqiManager.prototype.get_pm10 = function() {
    return this.data.data.map((item) => item['pm10']);
}

AqiManager.prototype.get_pm25 = function() {
    return this.data.data.map((item) => item['pm25']);
}
 
AqiManager.prototype.get_index = function(idx) {
    return this.data.data.map((item) => item[idx]);
}

// weatherbit api key 
var aqi_manager = new AqiManager();
async function load_aqi_data(lat, lng, start_date, end_date) {    
    await aqi_manager.load(
        lat,
        lng,
        start_date, 
        end_date
    );
}

async function get_aqi_data_by_idx(idx) {
    return await aqi_manager.get_index(idx);
}