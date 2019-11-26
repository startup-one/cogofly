var gTimerResetVegas = null;
var gBgImgs={
    '1280x1600': [
        {src: "{{ STATIC_URL|escapejs }}img/static/about.png"}
    ],
    '1600x1280': [
        {src: "{{ STATIC_URL|escapejs }}img/static/about.png"}
    ]
};
if (window.location.hostname.indexOf('dev')>=0) {
    var s = (new Date()).getTime().toString();
    for (var idx in gBgImgs) {
        for (var img in gBgImgs[idx]) {
            gBgImgs[idx][img].src = gBgImgs[idx][img].src+'?'+s
        }
    }
}
function resetVegas() {
    if ($(window).width()<776) {
        var imgs = gBgImgs['1280x1600'];
    } else {
        var imgs = gBgImgs['1600x1280'];
    }
    $('body').vegas({
            delay: 5000,
            timer: false,
            transitionDuration: 1500
        })
        .vegas('options', 'slides', imgs)
        .vegas('shuffle')
        .vegas('play');
}

$(document).ready(function() {
    gTimerResetVegas = window.setTimeout(resetVegas, 1);
});
$(window).resize(function(){
    try { $('body').vegas('pause'); } catch (e) {}
    if (gTimerResetVegas !== null) {
        window.clearTimeout(gTimerResetVegas);
    }
    gTimerResetVegas = window.setTimeout(resetVegas, 500);
});
