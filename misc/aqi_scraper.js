var weatherbit_key = 'c0756c0b51cd4bdb9e98c7582b3dfc06';
var aqicn_key = 'c0756c0b51cd4bdb9e98c7582b3dfc06';

async function get_last_from_index(data, index){
    let mapped = get_index_from_history(data, index);
    return mapped[mapped.length - 1];
}

async function get_index_from_history(data, index) { 
    return data.data.map((item) => item[index]);
}

async function get_history(lat, lng, start_date, end_date) {
    let request = `https://api.weatherbit.io/v2.0/history/airquality?lat=${lat}&lon=${lng}&start_date=${start_date}&end_date=${end_date}&tz=local&key=${weatherbit_key}`;
    let response = await fetch(request);
    let data = await response.json();
    return data;
}

async function get_today_history(lat, lng) {
    let today = new Date();
    let tomorrow = new Date();
    let yesterday = new Date();
    tomorrow.setDate(today.getDate() + 1);
    yesterday.setDate(today.getDate() - 1);
    let tomorrow_str = tomorrow.toISOString().split('T')[0];
    let yesterday_str = yesterday.toISOString().split('T')[0];
    return await get_history(lat, lng, yesterday_str, tomorrow_str);
}
