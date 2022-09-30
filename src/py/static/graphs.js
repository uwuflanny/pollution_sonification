async function create_graph(data,time, container_id, title = 'AQI') {

    Plotly.newPlot(container_id, [{
        x: time,
        y: data,
        type: 'stocks'
    }], 
        {
        width: 400,
        height: 250,
        margin: {
            t: 60,
            r: 30,
            l: 30,
            b: 50
        },
        // set title
        title: {
            text: title,
            font: {
                family: 'Arial',
                size: 16
            },
            xref: 'paper',
            x: 0.05,
        },
        }, {showSendToCloud: true}
    );


}