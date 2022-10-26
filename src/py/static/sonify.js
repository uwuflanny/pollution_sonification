
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
    let check = start_date == "" || end_date == "" || lat == "" || lng == "" || index == "" || start_date >= end_date;
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

async function sonify(){

    let payload = JSON.stringify(sonification_data);
    let leastest_aqi = sonification_data.data[sonification_data.data.length - 1];
    let location = sonification_data.location;

    let toast = Toastify({
        text: location + " - Sonification started!",
        duration: -1,
        close: true,
        gravity: "bottom",
        position: "right",
        style: {
            background: get_color(leastest_aqi),
            color: get_text_color(leastest_aqi)
        }
    });
    toast.showToast();

    let response = await fetch('/sonify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: payload
    });

    // get video
    let blob = await response.blob();
    let url = await window.URL.createObjectURL(blob);
    
    toast.hideToast();
    Toastify({
        text: location + " - Sonification done!",
        destination: url,
        duration: -1,
        newWindow: true,
        close: true,
        gravity: "bottom",
        position: "right",
        style: {
            background: get_color(leastest_aqi),
            color: get_text_color(leastest_aqi)
        }
    }).showToast();

}