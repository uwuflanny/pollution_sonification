
// this -> marker
async function show_offcanvas() {
    let options = this.options;
    let myOffcanvas = document.getElementById('sonificate');
    new bootstrap.Offcanvas(myOffcanvas).show();   
    $("#sonificate_p").attr("data-lat", options.lat);
    $("#sonificate_p").attr("data-lng", options.lng);
    $("#sonificate_title").text(options.title);
    $("#sonificate_p").text(options.aqi);
    $("#startDate").val("");
    $("#endDate").val("");
    $("#sonificate_plot").empty();
    $("#sonificate_action").hide();    
}

// TODO might need refactor remove duplication
async function sonify(){

    let start_date  = $("#startDate").val();
    let end_date    = $("#endDate").val();
    let lat         = $("#sonificate_p").attr("data-lat");
    let lng         = $("#sonificate_p").attr("data-lng");
    let index       = $("#sonificate_index").val();

    get_history(lat, lng, start_date, end_date).then(async (history)=>{            

        // request file
        let aqi = await history.get_index(index);
        let response = await fetch('/sonify', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({data: aqi})
        });

        // download audio
        let blob = await response.blob();
        let url = window.URL.createObjectURL(blob);
        $("#video_container").show();
        let video_container = $("#sonificate_video");
        video_container.show();
        video_container.attr("src", url);

    });

}

async function load_index(){

    let start_date  = $("#startDate").val();
    let end_date    = $("#endDate").val();
    let lat         = $("#sonificate_p").attr("data-lat");
    let lng         = $("#sonificate_p").attr("data-lng");
    let index       = $("#sonificate_index").val();
    
    // check data validity
    let check = start_date == "" || end_date == "" || lat == "" || lng == "" || index == "" || start_date >= end_date;
    $("#btn_sonify").prop("disabled", check);
    if(check) return;

    get_history(lat, lng, start_date, end_date).then(async (history) => {
        let aqis = await history.get_index('aqi');
        let time = await history.get_index('timestamp_local');
        create_graph(aqis, time, "sonificate_plot", `${index} from ${start_date} to ${end_date}`);
    });
    
}