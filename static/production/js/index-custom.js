(function ($) {

	new WOW().init();

	$('.box i').css({ 'margin-top':'3%' });
	$('.service-icon').css({ 'margin-top':'1%' }).hover(function() {
		$(this).css({ 'background': 'transparent' });
	});


	jQuery(window).load(function() {
		jQuery("#preloader").delay(100).fadeOut("slow", function(){
            /* On a passé PLUSIEURS HEURES à essayer de faire une animation
               qui s'affiche correctement partout, animation que je trouvais
               totalement inutile. Je cite :
               "Peux tu en parlant de clignoter d'enlever l'animation du départ
               sur l'accroche vous ne voulez plus...car cela déplaît aussi"
               ...
            var a = ($( window ).width()/12) | 0;
            if (a > 60) a = 60;
			$('#slogan h2')
				.animate({ fontSize: "1px" }, 100)
				.animate({ fontSize: a+"px" }, 2000,
					function() { $('#slogan h4').delay(500) });
			*/
		});
		/* Remontre le slogan, vu qu'il ne veut plus de son "effet" : */
		$('#slogan h4').show();
		jQuery("#load").delay(100).fadeOut("slow");
	});


    jQuery("#load").delay(100).fadeOut("slow");

	//jQuery to collapse the navbar on scroll
	$(window).scroll(function() {
		if ($(".navbar").offset().top > 50) {
			$(".navbar-fixed-top").addClass("top-nav-collapse");
		} else {
			$(".navbar-fixed-top").removeClass("top-nav-collapse");
		}
	});

	//jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$('.navbar-nav li a').bind('click', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $($anchor.attr('href')).offset().top
			}, 1500, 'easeInOutExpo');
			event.preventDefault();
		});
		$('.page-scroll a').bind('click', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $($anchor.attr('href')).offset().top
			}, 1500, 'easeInOutExpo');
			event.preventDefault();
		});
	});

    var gTimerResize;
    var handleScreenResized = function () {
        var a = ($( window ).width()/12) | 0,
            ratio = (($( window ).width() / $( window ).height())*10) | 0;
		if (ratio>10) {
			ratio = 20- (((ratio-10) * 0.7));
			$('#intro.intro').css({'padding': ratio+'% 0 0 0'});
		}
        if (a > 60) a = 60;
        $('#slogan h2').animate({ fontSize: a+"px" }, 60);
    };
    $(document).ready(function() {
        gTimerResize = window.setTimeout(handleScreenResized, 1);
    });
    $(window).resize(function(){
        if (gTimerResize !== null) {
            window.clearTimeout(gTimerResize);
        }
        gTimerResize = window.setTimeout(handleScreenResized, 500);
    });
})(jQuery);

