async function geocoder_search(){

    let geocoder = new google.maps.Geocoder();

    let location = $("#search_input").val();
    let index = $("#search_index").val();
    let min = $("#search_min").val();
    let max = $("#search_max").val();

    // move camera to location
    geocoder.geocode({
        'address': location
    }, function(results, status) {
        if (status == 'OK') {
            map.setCenter(results[0].geometry.location);
            map.setZoom(10);
        }
    });
}