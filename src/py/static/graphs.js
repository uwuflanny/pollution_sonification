async function create_graph(data,time, container_id, title = 'AQI') {

    Plotly.newPlot(container_id, [{
        x: time,
        y: data,
        type: 'bar',
        marker: {
            color: data.map(a => {
                return get_color(a);
            }
        )},
    }], 
        {
        margin: {
            t: 60,
            r: 30,
            l: 30,
            b: 50
        },
        title: {
            text: title,
            font: {
                family: 'Arial',
                size: 16
            },
            xref: 'paper',
            x: 0.05,
        },
        plot_bgcolor:"#4d4d4d",
        paper_bgcolor:"#111",
        font: {
            color: "white"
        },
        }, {showSendToCloud: true}

    );

}

async function create_graph_image(data,time, container_id, title = 'AQI') {

    Plotly.newPlot(container_id, [{
        x: time,
        y: data,
        type: 'bar',
        marker: {
            color: data.map(a => {
                return get_color(a);
            }
        )},
    }], 
        {
        margin: {
            t: 60,
            r: 30,
            l: 60,
            b: 140
        },
        xaxis: {
            // tickangle: 20,
            tickfont: {
                size: 24,
            }
        },
        yaxis: {
            tickfont: {
                size: 24,
            }
        },
        title: {
            text: title,
            font: {
                family: 'Arial',
                size: 30
            },
            xref: 'paper',
            x: 0.05,
        },
        plot_bgcolor:"#4d4d4d",
        paper_bgcolor:"#111",
        font: {
            color: "white"
        },

        }, {showSendToCloud: true}
    ).then(function(gd) {
        Plotly.toImage(gd, {format: 'png'})
            .then(function (url) {
                $("#"+container_id).show();
                $("#"+container_id).attr("src", url);
            })
    });


}