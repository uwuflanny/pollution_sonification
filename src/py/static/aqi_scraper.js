var weatherbit_key = 'c0756c0b51cd4bdb9e98c7582b3dfc06';
var aqicn_key = 'c0756c0b51cd4bdb9e98c7582b3dfc06';

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
    return this.data.map((item) => item[index]);
}

History.prototype.get_last_index = async function(index) {
    let mapped = this.get_index(index);
    return mapped[mapped.length - 1];
}

async function get_today_history(lat, lng) {
    let today = new Date();
    let tomorrow = new Date();
    let yesterday = new Date();
    tomorrow.setDate(today.getDate() + 1);
    yesterday.setDate(today.getDate() - 1);
    let tomorrow_str = tomorrow.toISOString().split('T')[0];
    let yesterday_str = yesterday.toISOString().split('T')[0];
    let history = new History(lat, lng, yesterday_str, tomorrow_str);
    await history.load();
    return history;
}

async function get_history(lat, lng, start_date, end_date) {
    let history = new History(lat, lng, start_date, end_date);
    await history.load();
    return history;
}