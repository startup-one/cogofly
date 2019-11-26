/* Code (C) Olivier Pons / HQF Development
 *
 * If you came here it's because you're interested with my code.
 * Don't hesitate to contact me for questions, formations, and services
 *
 * http://hqf.fr
 * http://olivierpons.fr
 */

function toggle_elements_visible(sel) {
    $(sel+':visible').slideUp(1000);
    $(sel+'.panel:hidden').slideDown(2000);
    return false;
}


function handleApiReady() {
    $(document).ready(function () {
        $('.gmaps-autocomplete').each(function(){
            var t=$(this)[0];
            new google.maps.places.Autocomplete(t, {});
            /* Trouvé sur stackoverflow :
             * http://stackoverflow.com/
             * questions/11388251/google-autocomplete-enter-to-select
             * Quand on appuyait sur "entrée" pour valider la sélection, cela
             * envoyait le formulaire. Maintenant ça semble ok :
             */
            google.maps.event.addDomListener(t, 'keydown', function(e) {
                if (parseInt(e.keyCode) === 13) {
                    e.preventDefault();
                }
            });
        });
        /* trouvé sur stackoverflow:
         * http://stackoverflow.com/
         * questions/15738259/disabling-chrome-autofill/
         * En fait il faut l'attribut autocomplete="off"
         * HACK : ce n'est plus "off", mais "false" !!!
         */
        $('input').each(function() {
            $(this).attr('autocomplete', 'false');
        });
        $('form').each(function() {
            $(this).attr('autocomplete', 'false');
        });
    });
}

if (typeof google === 'object' && typeof google.maps === 'object') {
    handleApiReady();
} else {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = 'https://maps.googleapis.com/maps/api/js' +
            '?key=AIzaSyCc0zrgx2mk-YPqzUvvpv4anNNWbMMk9EQ' +
            '&libraries=places' +
            '&callback=handleApiReady' +
            '&language=' + globCurrentLanguage;
    document.body.appendChild(script);
}


function initializeSelect2(language_code) {

    function item_or_text(obj) {
        if (typeof(obj.item)!='undefined') {
            return (obj.item.length ? obj.item : obj.text);
        }
        return obj.text;
    }

    function formatRepo(data) {
        if (data.loading) return data.text;
        return item_or_text(data);
    }

    function formatRepoSelection(item) {
        return item_or_text(item);
    }

    $('[data-select2-json!=""][data-select2-json]').each(function() {
        var url = $(this).attr('data-select2-json');
        var pg_size = $(this).attr('data-select2-page-size') | 30;
        var data = [{ id: 1, selected: true, item:'texte', text: 'texte' }];
        $(this).select2({
            tags: true,
            multiple: true,
            language: language_code,
            /*
            tokenSeparators: [',', ' '],
            */
            ajax: {
                url: url,
                dataType: 'json',
                delay: 300,
                data: function (params) {
                    return {
                        q: params.term, // -> q=[search term]
                        page: params.page // -> page=[no page]
                    };
                },
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        results: data.items,
                        pagination: {
                          more: (params.page * pg_size) < data.total
                        }
                    };
                },
                cache: true
            },
            // let our custom formatter work
            escapeMarkup: function (markup) { return markup; },
            minimumInputLength: 1,
            templateResult: formatRepo,
            templateSelection: formatRepoSelection,
            containerCssClass : 'select2'
        });

        $(this).select2('data', data, true);
    });
    /* Application du style bootstrap */
    $('.select2-container').css({'width':'100%'});
}


function initializeDateTimePicker(language_code) {
    moment.locale(language_code);
    $('.datetimepicker')
        .datetimepicker({
            viewMode: 'years',
            locale: language_code,
            format: 'L'
        })
        .datetimepicker({
            minDate: moment().subtract(80, 'years'),
            maxDate: moment().subtract(18, 'years')
        });
}

/* toggle nb éléments *après* l'élément en cours : */
function tg(a, nb){
    var a =$(a), b = a.next(), to_hide = b.is(':visible');
    if (to_hide) {
        for (var i=0; i<nb; i++) {
            b.stop().clearQueue().slideUp();
            b = $(b).next();
        }
    } else {
        for (var i=0; i<nb; i++) {
            b.stop().clearQueue().slideDown();
            b = $(b).next();
        }
    }
}

function togglePanel(el) {
    var btn = $('#'+$(el).attr('data-btn-to-show')),
        pnl = $('#'+$(el).attr('data-panel-to-show'));
    if ($(pnl).is(':visible')) {
        $(pnl).stop().clearQueue().slideUp();
        if (btn.attr('type')=='cancel') {
            $(btn.attr('data-btn-to-show')).stop().clearQueue().slideDown();
        } else {
            btn.stop().clearQueue().slideDown();
        }
    } else {
        var bCancel = pnl.find('button[type="cancel"]');
        bCancel.attr('data-btn-to-show', btn.attr('id'));
        bCancel.attr('data-panel-to-show', pnl.attr('id'));
        $(pnl).stop().clearQueue().slideDown();
        $(btn).stop().clearQueue().slideUp();
    }
    return false;
}

function travelTogglePanelAdd() {
    var f = $("#form-ajout-voyage"),
        v = $('#row-all-travels');
    if (f.is(':visible')) {
        f.stop().clearQueue().slideUp();
        v.stop().clearQueue().slideDown();
    } else {
        v.stop().clearQueue().slideUp();
        f.stop().clearQueue().slideDown();
    }
}

/* Code (C) Olivier Pons / HQF Development
 *
 * Si vous êtes ici c'est que vous voulez voir mon code !
 * Pour toute aide, formation, suggestions, n'hésitez pas à me contacter :
 *
 * http://hqf.fr
 * http://olivierpons.fr
 *
 * Toutes les fonctions précédentes sont des ébauches de la fonction qui suit,
 * il faudrait les supprimer pour ne fonctionner que sur celle qui suit, qui
 * est simple, évolutive et efficace :
 * L'objectif est d'avoir un bouton qui montre quelque chose, lié à un autre
 * bouton qui cache quelque chose *SANS AVOIR D'ID* car cela pose plein de
 * problèmes (être sûr d'avoir un id UNIQUE = bordel ÉNORME dans le templating)
 * ET qui soit évolutif :
 *
 * data-hqf-switch = "sélecteur/effet" ('/' "sélecteur/effet") x n
 * - avec les sélecteurs ayant des raccourcis :
 *                  ct(xx) -> closest(xx)
 *                  pt(xx) -> parent(xx)
 *                  nt(xx) -> next(xx)
 *                  pv(xx) -> prev(xx)
 * - avec les effets ayant des raccourcis :
 *                  u = slideUp(), d = slideDown()
 *                  h = hide(), s = show()
 * - si on met X devant l'effet, c'est remplacé par stop().clearQueue()
 *   exemple : Xu -> stop().clearQueue().slideUp()
 * - si on met O devant l'effet, c'est le même que X mais on ramène l'écran
 *   tout à fait en haut
 *
 *   exemple :   data-hqf-switch="$.nt().nt()/Xd"
 *   exécutera : $(this).next().next().stop().clearQueue().slideDown();
 *
 * (C) 2016 / Olivier Pons / HQF Development
 */
$(document).ready(function () {
    var sw = function(a, b) {
        var t = ['u', 'slideUp()',  'd', 'slideDown()',
                 'o', 'fadeOut()',  'i', 'fadeIn()',
                 'h', 'hide()',     's', 'show()',
                 'k', 'hide().remove()'];
        var sx = function(a) {
            for (var i = 0; i<t.length; i+=2)
                if (a==t[i]) return t[i+1];
            return a;
        };
        var r = (typeof(a) != 'undefined' ? (a || b) : b);
        if ((typeof(r) == 'string') && (r =='$')) {
            r = '$(this)';
        }
        if ((typeof(r) == 'string') && (r.length==2) && (r[0]=='X')) {
            r = 'stop().clearQueue().' + sx(r[1]);
        } else if ((typeof(r) == 'string') && (r.length==2) && (r[0]=='O')) {
            $('html, body').animate({
                scrollTop:$('body').offset().top
            }, 500);
            r = 'stop().clearQueue().' + sx(r[1]);
        } else {
            r = sx(r);
        }
        return r.replace('$.', '$(this).')
                .replace(/\.ct\(/g, '.closest(')
                .replace(/\.cd\(/g, '.children(')
                .replace(/\.sb\(/g, '.siblings(')
                .replace(/\.ft\(/g, '.first(')
                .replace(/\.fd\(/g, '.find(')
                .replace(/\.pt\(/g, '.parent(')
                .replace(/\.pa\(/g, '.prevAll(')
                .replace(/\.nt\(/g, '.next(')
                .replace(/\.pv\(/g, '.prev(');
    };
    $('[data-hqf-toggle]').click(function() {
        var t = $(this).attr('data-hqf-toggle').split('/'),
            i = 0;
        while (i < t.length) {
            var ev = 'var a = '+sw(t[i++], '$')+';',
                d=sw(t[i++], 'd'),
                u=sw(t[i++], 'u');
            eval(ev);
            //console.log('a = ', a, ', a.is(:visible)', a.is(':visible'));
            //console.log('d = ', d, ', u', u);
            if (a.is(':visible')) {
                eval('a.stop().clearQueue().'+u);
            } else {
                eval('a.stop().clearQueue().'+d);
                /* Scroll to the "opening" element: */
                $('html, body').animate({
                    scrollTop:a.offset().top - 80
                }, 500);
            }
        }
    });
    $('[data-hqf-switch]').click(function(e) {
        var target = $(e.target);
        if ($.inArray(target.get(0).tagName.toLowerCase(),
            ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'i'])===-1
        ) {
            if (target.filter('[data-hqf-switch]').length===0) {
                return;
            }
        }
        var t = $(this).attr('data-hqf-switch').split('/'),
            i = 0;
        if (t % 2) {
            alert('Erreur inattendue, merci de contacter le support');
            return;
        }
        while (i < t.length) {
            var ev = sw(t[i++], '$')+'.'+sw(t[i++], 'd')+';';
            //console.log(ev);
            eval(ev);
        }
    });
});

/* Onglet des voyages */
function handleTravelsReady() {
    $(document).ready(function () {
        /* Si erreur, sélectionner l'onglet */
        var t=$('div.alert.alert-danger').closest('div.tab-pane');
        if (t.length) {
            t = $('a[href="#'+t.attr('id')+'"]');
            if (t.length) {
                $($(t[0]).attr('href')).find('.travels-summary').hide();
                $(t[0]).click();
                return;
            }
        }

        var t=getCookie('travels_tab'),
            fn=function (a){return document.getElementById(a)},
            d, btn;
        if ((typeof(t)!='undefined') && (parseInt(t))) {
            d = fn("travels-future"),
            btn = fn("btn-travels-future");
        } else {
            d = fn("travels-past"),
            btn = fn("btn-travels-past");
        }
        if ((d != null) && (btn != null)) {
            d.className = d.className + " active in";
            btn.className = btn.className + " active";
        }
    });
}

/*-------------------------------------------------------------
 * search
 *
 */
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
};

function toggle(a, b) {
    var a = $(a),  b = $(b);
    if ($(b).is(':visible')) {
        $(a).stop().clearQueue().fadeIn();
        $(b).stop().clearQueue().slideUp();
    } else {
        $(a).stop().clearQueue().fadeOut();
        $(b).stop().clearQueue().slideDown();
    }
}
$(document).ready(function(){
    $('.form-search').submit(function() {
        var idx = $('#search-pills').find("li.active").index()+1;
        window.location.href = window.location.pathname+'?'+
            $(this).serialize()+'&tab='+idx;
        return false;
    });
});

function travelsTabChange(idx, el) {
    var f = $('#form-ajout-voyage'),
        e = $('#'+el),
        g = e.find('.grid'),
        ch = e.find('.grid').children();
    e.find('.grid').css('height', parseInt($(ch[0]).css('min-height')));
    setCookie('travels_tab', idx, 15);
    if (f.is(':visible')) {
        f.find("button[type='cancel']").click();
    }
    setTimeout(function() {
        g.isotope({sortBy: 'original-order'});
    }, 600);
}
function travelsSetIsPast(el) {
    var a = $('#btn-travels-past').hasClass('active');
    $(el).find('[name="is_past"]').prop('checked', a).val(a ? 'on' : '');
    return false;
}

function initializeILike(url_evt, url_person) {
    var fnDisable = function(self) {
        /* -------- rendre le bouton disabled -------- */
        self.addClass("disabled").unbind('click');
        self.find('button').each(function () {
            $(this).addClass("disabled");
        });
        /* -------- */
    };

    var span_i_like=$('button.ilike');
    span_i_like.on('click', function() {
        var self = $(this), pk, url;
        pk = self.attr('data-liked');
        if (typeof(pk)=='undefined') {
            /* liker une personne (!= liker un evt) */
            pk = self.attr('data-person');
            url = url_person;
        } else {
            url = url_evt;
        }
        self.fadeOut();
        $.ajax({
            url: url.replace("0", pk),
            data: {pk: pk},
            cache: false,
            crossDomain: true,
            dataType: 'json',
            method: 'get'
        }).done(function(data){
            fnDisable(self);
            var a = "fa fa-thumbs-"+(data.liked ? "" : "o-")+ "up fa-fw";
            self.find('i').each(function () {
                $(this).removeClass().addClass(a+" disabled");
            });
            self.fadeIn();
        }).error(function(){
            console.log("Erreur!");
        }).complete(function(a,b,c){
            console.log(a, b, c);
        });
    });

    span_i_like.each(function() {
        var up=false;
        $(this).find('i').each(function () {
            if ($(this).attr('class').indexOf('thumbs-up')>0) {
                up = true;
            }
        });
        if (up) { fnDisable($(this)); }
    });

}

function ajaxSendId(url, pk, fnCallBack) {
    $.ajax({
        url: url.replace("0", pk),
        cache: false,
        crossDomain: true,
        dataType: 'json',
        method: 'get'
    }).done(function(data){
        fnCallBack();
    }).error(function(){
        //console.log("Erreur!");
    }).complete(function(a,b,c){
        //console.log(a, b, c);
    });
    return false;
}

function initializeInvite(url) {
    $('button.invite').each(function() {
        $(this).on('click', function() {
            return ajaxSendId(url,
                $(this).attr('data-invite'),
                /* callback quand json ok */
                function (){
                    window.location.reload(true);
                });
        });
    });
}

function initializeRelationRemove(url) {
    $('[data-relation-remove]').each(function() {
        $(this).on('click', function() {
            return ajaxSendId(url,
                $(this).attr('data-relation-remove'),
                /* callback quand json ok */
                function (){
                    window.location.reload(true);
                });
        });
    });
}

function flash(t, b) {
    t.html(b).fadeOut(function() {
        t.fadeIn(200).fadeOut().fadeIn(200).fadeOut().fadeIn(200);
    });
}

function notificationsApplyEffects(sing, plur) {
    $('.'+sing+'-summary').each(function() {
        var self = $(this),
            t = self.find('button.slide');
        if (t.length==0) {
            t = $(this);
            t.hover(
                function () {
                    //$(this).css({'outline': 'solid 3px #337ab7'});
                },
                function() {
                    //$(this).css({ 'outline': '' })
                }
            );
        }
        t.click(function(e) {
            if ($(e.target).filter('[data-toggle]').length) {
                /* Si on bouton alors on ne fait rien */
                return;
            }
            var c = $(this).closest('.'+sing+'-summary'),
                id = c.attr('id').split('-');
            id = parseInt(id[id.length-1]);
            var dst = $('body').find('#'+sing+'-full-'+id);
            if (typeof(dst)!='undefined') {
                $('.'+plur+'-summary').slideUp(/*function() {
                    self.find('h4').css({'font-size': '16px',
                                         'font-weight': 'lighter' });
                }*/);
                dst.slideDown();
            }
        });
    });
    /* !! */
    $('div.conversation-summary').click(function(e) {
        if ((!$(e.target).is(':button')) &&
             !($(e.target).parent().is(':button'))) {
            $(this).find(':button.btn-validate').click();
            return false;
        }
    });
}
function notificationsDiminue(onglet) {
    var a = $(onglet).find('.badge-new'),
        b = parseInt(a.html())- 1,
        c = $('#menu-notifications').find('.badge-new'),
        d = parseInt(c.html())- 1;
    flash(a, b);
    flash(c, d);
}
function initializeMarkMessageRead(url) {
    var localClick = function(e) {
        var self=$(this),
            t = self.find('button.slide');
        if ($(e.target).is('button')) {
            /* on a cliqué sur un bouton = rien faire ici : */
            console.log('on a cliqué sur un bouton = rien faire ici');
            $(this).one('click', localClick);
            return;
        }
        e.stopPropagation();
        $(this).find('[data-msg]').each(function() {
            ajaxSendId(url,
                $(this).attr('data-msg'),
                /* callback quand json ok */
                function (){
                    self.find('.timeline-badge').each(function() {
                        $(this).remove();
                    });
                    t.children('.conv-msg-notread').each(function() {
                        $(this).animate(
                            { width: "toggle" },
                            2000, 'swing',
                            function() { $(this).remove(); }
                        );
                    });
                    notificationsDiminue('#btn-tab-messages');
                    //window.location.reload(true);
                });
        });
    };
    $('.msg-notread').each(function() {
        var t=$(this);
        t.one('click', localClick);
    });
}

function initializeMarkLikeRead(url) {
    $('button.mark-like-read').each(function() {
        $(this).one('click', function() {
            return ajaxSendId(
                url, $(this).attr('data-like-pk'),
                /* callback si json ok */
                function () {
                    var a = $('#btn-tab-likes').find('.badge-new'),
                        b = parseInt(a.html())- 1,
                        c = $('#menu-notifications').find('.badge-new'),
                        d = parseInt(c.html())- 1;
                    if (b || d) {
                        flash(a, b);
                        flash(c, d);
                    } else {
                        window.location.reload(true);
                    }
                }
            );
        });
    });
}

function travelsInitializePreview(url) {
    //Au moment d'envoyer, ajouter l'onglet sur lequel on est :
    $('[action="'+url+'"]').submit(function(){
        travelsSetIsPast($(this));
    });
    $("#form-ajout-voyage").find('button[type="cancel"]')
            .unbind('click')
            .click(travelTogglePanelAdd);
}

function contactsRefreshGrid() {
    var e = $('body').find('.contacts').find('.grid');
    setTimeout(function() {
        e.isotope({sortBy: 'original-order'});
    }, 400);
    return false;
}

function checkUncheckAll(cls) {
    $(cls).unbind('click').click(function() {
        var self=$(this),
            c = !!self.is(':checked');
        self.closest('form').find("input:checkbox:not('"+cls+"')").each(function() {
            if ($(this)!=self) {
                $(this).prop('checked', c);
            }
        });
    });
}

function selectPicturesInitialize(labelCancel) {
    $('form').each(function() {
        $(this).find('input[accept="image/*"]').each(function() {
            var ref = $(this).parent(),
                img = $(this).parent().find('img');
            if (img.length==0) {
                ref = $(this).parent().parent();
                img = $(this).parent().parent().find('img');
            }
            var src_original = img.attr('src');
            $(this).after(
                $('<button />')
                    .addClass('image-cancel')
                    .html(labelCancel)
                    .hide()
                    .click(function(e) {
                        e.preventDefault();
                        ref.find('input[accept="image/*"]').val('').fadeIn();
                        ref.find('img')
                            .stop().clearQueue()
                            .slideUp(function() {
                                $(this).attr('src', src_original);
                                $(this).slideDown();
                            });
                        $(this).fadeOut();
                    })
            );
            $(this).on('change', function (e) {
                var files = $(this)[0].files;
                if (files.length > 0) {
                    var file = files[0],
                        obj = window.URL.createObjectURL(file),
                        t = $(this);
                    ref.find('img').attr('src', obj).slideDown();
                    t.fadeOut();
                    t.next('.image-cancel').fadeIn();
                }
            });
        });
    });
}


/*
    http://stackoverflow.com/questions/
    5448545/how-to-retrieve-get-parameters-from-javascript
 */
function getSearchParameters() {
      var prmstr = window.location.search.substr(1);
      return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
}
function transformToAssocArray( prmstr ) {
    var params = {};
    var prmarr = prmstr.split("&");
    for ( var i = 0; i < prmarr.length; i++) {
        var tmparr = prmarr[i].split("=");
        params[tmparr[0]] = tmparr[1];
    }
    return params;
}
var gQueryParams = getSearchParameters();

/**
 * for CheckboxSelectMultipleBootstrap component
 */
var gModalCheckboxesHintShown = false;
function modalCheckboxesShowHintIfNotDone() {
    if (gModalCheckboxesHintShown) {
        return;
    }
    gModalCheckboxesHintShown = true;
}
function modalCheckboxesClickOk(el) {
    var modified = false, nb_checked = 0, modal=$(el).closest('.modal-dialog');
    modal.find('input[type="checkbox"]').each(function () {
        modified = modified | Boolean($(this).data('modified'));
        if ($(this).is(':checked')) {
            nb_checked++;
        }
    });
    var sp = $($(el).data('label-to-change')).find('span');
    if (modified) {
        sp.css({'color': 'red'});
        sp.html('(<b>' + nb_checked + '</b>)');
    } else {
        // NOT modified:
        sp.css({'color': ''});
        sp.html('(<b>' + nb_checked + '</b>)');
    }
}
function modalCheckboxesClickOkInitialize(lbl) {
    var t = $('#'+lbl);
    t.find('input[type="checkbox"]').each(function() {
        var original = Boolean($(this).is(':checked'));
        $(this).data('modified', false);
        $(this).click(function() {
            // modified becomes true if different from original
            $(this).data('modified',
                ($(this).is(':checked')!=original)
            );
        });
    });
    var nb= t.find('input[checked="checked"]').length;
    $('#modal-field-'+lbl).find('button.btn-validate').data(
        'label-to-change', 'label[for="'+lbl+'"]'
    );
    $('label[for="'+lbl+'"]').append(
        $("<span />")
            .addClass('total-checked')
            .css({'font-size': 'smaller',
                  'font-weight': 'normal'})
            .html('(<b>' + nb + '</b>)')
    );
}
