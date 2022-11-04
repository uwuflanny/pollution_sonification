
// i'm sorry for your eyes

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

async function propose_tutorial(){
    
    let toast = Toastify({
        text: "Quick tutorial? (click to start)",
        close: true,
        duration: -1,
        gravity: "bottom",
        position: "right",
        onClick: function(){
            start_tutorial();
            toast.hideToast();
        }
    }).showToast();

    let handler = function(){
        toast.hideToast();
        $("#offcanvas_btn_sonify").off('click', handler);
    }

    $("#offcanvas_btn_sonify").click(handler);
  
}

async function start_tutorial() {

    // clear present markers
    hide_offcanvas();
    layerGroup.clearLayers();

    let toast = get_tutorial_toast(`Click on any place of the map to inspect its current air quality, you can also search for a specified location.`);
    toast.showToast();

    let callback = function(){
        map.off('layeradd', callback);
        toast.hideToast();
        tutorial_2();
    }

    // run callback when a new marker is added
    map.on('layeradd', callback);

}

async function tutorial_2(){

    let toast = get_tutorial_toast("Click on any marker to start personalizing the sonification.");
    toast.showToast();

    let done = false;
    load_offcanvas = new Proxy(load_offcanvas, {
        apply: function(target, thisArg, argumentsList) {
            target.apply(thisArg, argumentsList);
            if(!done){
                done = true;
                toast.hideToast();
                tutorial_3();  
            }
        }
    });

}

async function tutorial_3(){

    let finaltoast = get_tutorial_toast("Here you can choose your sonification parameters, when you are ready, click the sonify button to start the sonification.", {close: true});
    finaltoast.showToast();

    let handler = function(){
        finaltoast.hideToast();
        $("#offcanvas_btn_sonify").off('click', handler);
        Toastify({
            text: "Have Fun :D",
            duration: 3000,
            close: false,
            gravity: "bottom",
            position: "right",
        }).showToast();
    }

    $("#offcanvas_btn_sonify").click(handler);

}