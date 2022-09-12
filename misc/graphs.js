async function today_aqi_graph(lat, lng) {

    // TODO TEST WITH FIRST DAY OF MONTH
    // get today and yesterday date as year-month-day
    let today = new Date();
    let yesterday = new Date();
    yesterday.setDate(today.getDate() - 1);
    let today_str = today.toISOString().split('T')[0];
    let yesterday_str = yesterday.toISOString().split('T')[0];


    // get history
    let request = `https://api.weatherbit.io/v2.0/history/airquality?lat=${lat}&lon=${lng}&start_date=${yesterday_str}&end_date=${today_str}&tz=local&key=c0756c0b51cd4bdb9e98c7582b3dfc06`;
    let response = await fetch(request);
    let response_data = await response.json();    

    
    let time = response_data.data.map((item) => item['timestamp_local']);
    let aqis = response_data.data.map((item) => item['aqi']);
    
    Plotly.newPlot("graph_plot", [{
        x: time,
        y: aqis,
        type: 'stocks'
    }]);

}