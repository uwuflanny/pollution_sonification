async function create_today_graph(history, index) {

    let time = await get_index_from_history(history, 'timestamp_local');
    let aqis = await get_index_from_history(history, index);

    Plotly.newPlot("graph_plot", [{
        x: time,
        y: aqis,
        type: 'stocks'
    }]);

}