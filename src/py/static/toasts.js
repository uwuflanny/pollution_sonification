
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

function get_tutorial_toast(text, extra = {}){
    return Toastify({
        text: text,
        duration: -1,
        close: false,
        gravity: "bottom",
        position: "right",
        style: {
            maxWidth: "33%",
        },
        ...extra
    });
}