
async function show_offcanvas() {
    // this -> marker
    document.getElementById("mySidebar").style.width = screen.width <= 500 ? "100%" : "25%";
    let options = this.options;
    $("#offcanvas_location").text(options.location);
    $("#offcanvas_aqi").attr("data-lat", options.lat);
    $("#offcanvas_aqi").attr("data-lng", options.lng);
    $("#offcanvas_aqi").text("AQI - " + options.aqi + "     " + get_emoji(options.aqi));
    $("#offcanvas_plot").hide();

    let dates = await get_nearest_dates();
    $("#offcanvas_start_date").val(dates[0]);
    $("#offcanvas_end_date").val(dates[1]);

    load_index();
}

function hide_offcanvas() {
    document.getElementById("mySidebar").style.width = "0";
}


// TODO might need refactor remove duplication
async function sonify(){

    let start_date  = $("#offcanvas_start_date").val();
    let end_date    = $("#offcanvas_end_date").val();
    let lat         = $("#offcanvas_aqi").attr("data-lat");
    let lng         = $("#offcanvas_aqi").attr("data-lng");
    let index       = $("#offcanvas_index").val();

    get_history(lat, lng, start_date, end_date).then(async (history)=>{            

        let aqi = await history.get_index(index);
        let times = await history.get_index('timestamp_local');
        let payload = JSON.stringify({idx: index, data: aqi, days: times});

        let response = await fetch('/sonify', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: payload
        });

        // get video
        let blob = await response.blob();
        let url = await window.URL.createObjectURL(blob);
        window.open(url)

    });

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
    });
    
}