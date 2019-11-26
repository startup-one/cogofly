var gTimerResetVegas = null;
var gBgImgs={
    '1280x1600': [
        {src: '/static/img/1280x1600/bg1b.jpg'},
        {src: '/static/img/1280x1600/bg1a.jpg'}
    ],
    '1600x1280': [
        {src: '/static/img/1600x1280/bg1b.jpg'},
        {src: '/static/img/1600x1280/bg1a.jpg'}
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
    if (!$.vegas) return;
    if ($(window).width()<776) {
        var imgs = gBgImgs['1280x1600'];
    } else {
        var imgs = gBgImgs['1600x1280'];
    }
    $('#intro').vegas({
            delay: 5000,
            timer: false,
            transitionDuration: 1500
        })
        .vegas('options', 'slides', imgs)
        .vegas('play');
}

$(document).ready(function() {
    var fnColleDeuxBlocsDuBas= function() {
        //$('#future-box-1').css({'border-bottom': 0});
        //$('#future-box-2').css({'border-top': '1px solid #AAA'});
        $('.box-bloc').css({'margin-bottom': 0});
    };

    /* (!!) Recalcul AVANT vegas car vegas empêche l'application du padding */
    var h = $( window ).height(),
        ratio = (($( window ).width() / h)*10) | 0;
    console.log('ratio : ',ratio, ', h=', h);
    if (h<790) {
        fnColleDeuxBlocsDuBas();
    }
    if (ratio>10) {
        var pc = 20- (((ratio-10) * 0.7));
        $('#intro.intro').css({'padding': pc+'% 0 0 0'});
        var t = ratio - 10;
        $('div.row.row-eq-height.box-bloc').css({'margin-top': t+'%'});
    } else if (ratio<10) {
        var ratio = (($( window ).width() / $( window ).height())*100) | 0;
        if (ratio>=56) {
            console.log('ratio= ', ratio);
            console.log('ratio-56= ', ratio-56);
            console.log('30-((ratio-56)*2)= ', 30-((ratio-56)*2));
            var t = 30-((ratio-56)*2);
            if (t>0) {
                $('div.row.row-eq-height.box-bloc').css({'margin-top': t+'%'});
            }
        }
    }
    return;
    gTimerResetVegas = window.setTimeout(resetVegas, 1);
});
$(window).resize(function(){
    try { $('#intro').vegas('pause'); } catch (e) { console.log(e); }
    if (gTimerResetVegas !== null) {
        window.clearTimeout(gTimerResetVegas);
    }
    gTimerResetVegas = window.setTimeout(resetVegas, 500);
});
