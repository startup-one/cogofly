/* Fonction pour 'toggle' un élément, qui prend un objet "option" qui peut
 * contenir deux propriétés 'start' et 'end' qui sont des fonctions appelées
 * respectivement au début et à la fin de l'animation
 */
var gFnToggle = function (el, opt) {
    var fnExe = function(m, o, idx) {
        if (typeof(o)=='object') {
            if (typeof(o[idx])=='function') {
                o[idx](m);
            }
        }
    };
    var me=$(el);
    me.animate({
        height: "toggle"
    }, {
        duration: 2500,
        specialEasing: {
            width: "easeOutBounce",
            height: "easeOutBounce"
        },
        start: $.proxy(function () {
            fnExe(this.me, this.opt, 'start');
        }, {'me': me, 'opt': opt }),
        complete: $.proxy(function () {
            fnExe(this.me, this.opt, 'end');
        }, {'me': me, 'opt': opt })
    });
};
$(document).ready(function () {
    $('#register form').submit(function () {
        $('#register').slideUp('fast');
        $('#signup-page').slideDown('fast', function () {
            $('html, body').scrollTo(
                $('#signup-page').offset().top - 10, 'slow', 'easing'
            );
        });
        return false;
    });

    $('#signup-page-cancel').submit(function () {
        $('#signup-page').slideUp(1500, function () {
            $('html, body').scrollTo(0, 'slow', 'easing');
        });
        $('#register').slideDown(2000);
        return false;
    });

    if ($('.errorlist').length) {
        try { $('body').vegas('pause'); } catch (e) {}
        $('#signup-page').slideDown({
            duration: 1000,
            easing: 'swing',
            complete: function () {
                $('html, body').scrollTo(
                    $('#signup-page').offset().top - 10, 'slow', 'easing'
                );
                try { $('body').vegas('play'); } catch (e) {}
            }
        });
    } else if (
        ($('#registration-done-check-email').length==0)
        && ($('#registration-validated').length==0)
    ) {
        setTimeout(function() { $('#register').slideDown(); }, 1000);
    }
});