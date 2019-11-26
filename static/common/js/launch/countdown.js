var gDrawTimerHandle = null;

function drawTimer() {
    var s = ($(window).width()<822 ? '-s' : ''),
        c = $(".digits"),
        t = new Date();
        t.setSeconds(t.getSeconds() + 1);
    c.children().remove();
    c.html('').empty().countdown({
        format: "dd:hh:mm:ss",
        //endTime: new Date("03/23/2016 23:59:59"),
        endTime: t,
        image: '{{ STATIC_URL|escapejs }}img/countdown/digits-min'+s+'.png',
        digitWidth: (s!='' ? 34 : 68),
        digitHeight:  (s!='' ? 45 : 90),
        imgs_separators: [
            '{{ STATIC_URL|escapejs }}img/countdown/digits'+s+
                '-jj'+(globLanguage=='fr'? '-fr':'')+'.png',
            '{{ STATIC_URL|escapejs }}img/countdown/digits'+s+'-hh-mm.png',
            '{{ STATIC_URL|escapejs }}img/countdown/digits'+s+'-hh-mm.png'
        ],
        forMobile: (s!='')
    });
        clearInterval(intervals.main);
    gDrawTimerHandle = null;
}


$(document).ready(function () {
    gDrawTimerHandle = window.setTimeout(drawTimer, 1);
});


$(window).resize(function(){
    if (typeof(intervals)!=='undefined') {
        $(".digits").attr('started', false);
        clearInterval(intervals.main);
    }
    if (gDrawTimerHandle !== null) {
        window.clearTimeout(gDrawTimerHandle);
    }
    gDrawTimerHandle = window.setTimeout(drawTimer, 500);
});
