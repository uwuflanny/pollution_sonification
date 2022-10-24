var weatherbit_key  = 'fc97477c45744fbfb603cc525e8f5279';
var aqicn_key       = 'd7997a4e2fa35a67576fa7e7e766f6f226cf59f5';


async function get_all_stations() {
    let url = `https://api.waqi.info/v2/map/bounds?latlng=-90,-180,90,180&networks=all&token=${aqicn_key}`;
    let response = await fetch(url);
    let data = await response.json();
    return data.data;
}

function History(lat, lng, start_date, end_date) {
    this.lat = lat;
    this.lng = lng;
    this.start_date = start_date;
    this.end_date = end_date;
}

History.prototype.load = async function() {
    let request = `https://api.weatherbit.io/v2.0/history/airquality?lat=${this.lat}&lon=${this.lng}&start_date=${this.start_date}&end_date=${this.end_date}&tz=local&key=${weatherbit_key}`;
    let response = await fetch(request);
    let resp_data = await response.json();
    this.data = resp_data.data;
}

History.prototype.get_index = async function(index) {
    let arr = this.data.map((item) => item[index]);
    return arr.reverse();
}

async function get_nearest_dates() {
    let today = new Date();
    let tomorrow = new Date();
    let yesterday = new Date();
    tomorrow.setDate(today.getDate() + 1);
    yesterday.setDate(today.getDate() - 1);
    let tomorrow_str = tomorrow.toISOString().split('T')[0];
    let yesterday_str = yesterday.toISOString().split('T')[0];
    return [yesterday_str, tomorrow_str];
}

async function get_today_history(lat, lng) {
    let dates = await get_nearest_dates();
    let history = new History(lat, lng, dates[0], dates[1]);    
    await history.load();
    return history;
}

// TODO FIX SELECTING TODAY VALUE, MUST GET ALL DATA
async function get_history(lat, lng, start_date, end_date) {
    let history = new History(lat, lng, start_date, end_date);
    await history.load();
    return history;
}