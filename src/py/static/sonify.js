
function show_offcanvas() {
    let sidebar = $("#mySidebar");
    sidebar.prop("enabled", true);
    sidebar.css("width", screen.width <= 500 ? "100%" : screen.width <= 1000 ? "50%" : "25%");
}
function hide_offcanvas() { 
    let sidebar = $("#mySidebar");
    sidebar.prop("enabled", false);
    sidebar.css("width", "0px");
}
function width_change() { 
    if($("#mySidebar").prop("enabled")) show_offcanvas();
} 

async function load_offcanvas() {

    let options = this.options;
    $("#offcanvas_location").text(options.location);
    $("#offcanvas_aqi").attr("data-lat", options.lat);
    $("#offcanvas_aqi").attr("data-lng", options.lng);
    $("#offcanvas_aqi").text("AQI - " + options.aqi + "\t" + get_emoji(options.aqi));
    $("#offcanvas_plot").hide();

    let dates = await get_nearest_dates();
    $("#offcanvas_start_date").val(dates[0]);
    $("#offcanvas_end_date").val(dates[1]);

    show_offcanvas();
    load_index();

}

async function load_index(){

    let start_date  = $("#offcanvas_start_date").val();
    let end_date    = $("#offcanvas_end_date").val();
    let lat         = $("#offcanvas_aqi").attr("data-lat");
    let lng         = $("#offcanvas_aqi").attr("data-lng");
    let index       = $("#offcanvas_index").val();
    
    get_history(lat, lng, start_date, end_date, index).then(async (history) => {

        let aqis = await history.get_index(index);
        let time = await history.get_index('timestamp_local');
        create_graph_image(aqis, time, "offcanvas_plot", `${index} from ${start_date} to ${end_date}`);
        $("#offcanvas_btn_sonify").show();

        sonification_data = {
            idx: index,
            data: aqis,
            days: time,
            location: $("#offcanvas_location").text()
        }

    }).catch(async (error) => {
        
        $("#offcanvas_btn_sonify").hide();
        $("#offcanvas_plot").attr("src", "");
        console.log(error);

    });
    
}

async function sonify(){

    let payload = JSON.stringify(sonification_data);
    let leastest_aqi = sonification_data.data[sonification_data.data.length - 1];
    let location = sonification_data.location;

    let start_toast = await get_sonification_toast(location, "Sonification started", leastest_aqi);
    start_toast.showToast();

    await fetch('/sonify', {

        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: payload

    }).then(async function(response) {
    
        if (!response.ok) throw Error(response.statusText);

        let blob = await response.blob();
        let url = URL.createObjectURL(blob);
        let success_toast = await get_sonification_toast(location, "Click to play", leastest_aqi, {destination: `/video?src=${url}`, newWindow: true});
        success_toast.showToast();

    }).catch(async function(error) {

        let error_toast = await get_sonification_toast(location, "Sonification failed", leastest_aqi);
        error_toast.showToast();
        console.log(error);

    }).finally(async function() {

        start_toast.hideToast();

    });

}