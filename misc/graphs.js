async function today_aqi_graph(container_id, lat, lng) {

    // today date year-month-day
    let today = new Date();
    let today_date = `${today.getFullYear()}-${today.getMonth()+1}-${today.getDay()}`;
    // yesterday date year-month-day
    let yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    let yesterday_date = `${yesterday.getFullYear()}-${yesterday.getMonth()+1}-${yesterday.getDay()}`;

    // get history
    let request = `https://api.weatherbit.io/v2.0/history/airquality?lat=${lat}&lon=${lng}&start_date=${yesterday_date}&end_date=${today_date}&tz=local&key=c0756c0b51cd4bdb9e98c7582b3dfc06`;
    let response = await fetch(request);
    let aqis = await response.json();    
    
    var trace = {
        x: aqis,
        type: 'histogram',
    };
    var data = [trace];
    Plotly.newPlot(container_id, data);

}