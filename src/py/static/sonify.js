
function show_offcanvas() { document.getElementById("mySidebar").style.width = screen.width <= 500 ? "100%" : (screen.width <= 1000 ? "50%" : "25%"); }
function hide_offcanvas() { document.getElementById("mySidebar").style.width = "0"; }

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
    
    // check data validity
    let start = new Date(start_date);
    let end = new Date(end_date);
    let diff = Math.abs(end - start);
    let days = Math.ceil(diff / (1000 * 60 * 60 * 24));
    let check = start_date == "" || end_date == "" || lat == "" || lng == "" || index == "" || start_date >= end_date || days > 2;
    $("#offcanvas_btn_sonify").prop("disabled", check);
    if(check) return;

    get_history(lat, lng, start_date, end_date).then(async (history) => {

        let aqis = await history.get_index(index);
        let time = await history.get_index('timestamp_local');
        create_graph_image(aqis, time, "offcanvas_plot", `${index} from ${start_date} to ${end_date}`);

        sonification_data = {
            idx: index,
            data: aqis,
            days: time,
            location: $("#offcanvas_location").text()
        }

    });
    
}

async function get_sonification_toast(location, status, aqi, extra = {}){
    return Toastify({
        text: location + " - " + status,
        duration: -1,
        close: true,
        gravity: "bottom",
        position: "right",
        style: {
            background: get_color(aqi),
            color: get_text_color(aqi)
        },
        ...extra
    });
}

async function sonify(){

    let payload = JSON.stringify(sonification_data);
    let leastest_aqi = sonification_data.data[sonification_data.data.length - 1];
    let location = sonification_data.location;

    let start_toast = await get_sonification_toast(location, "Sonificatio started", leastest_aqi);
    start_toast.showToast();

    await fetch('/sonify', {

        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: payload

    }).then(async function(response) {
    
        if (!response.ok) throw Error(response.statusText);

        let blob = await response.blob();
        let url = await window.URL.createObjectURL(blob);
        let success_toast = await get_sonification_toast(location, "Click to play", leastest_aqi, {destination: url, newWindow: true});
        success_toast.showToast();

    }).catch(async function(error) {

        let error_toast = await get_sonification_toast(location, "Sonification failed", leastest_aqi);
        error_toast.showToast();
        console.log(error);

    }).finally(async function() {

        start_toast.hideToast();

    });

}