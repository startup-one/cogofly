# coding=UTF-8



import json
import linecache

import sys
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.urls import resolve, Resolver404, reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import translation
from django.utils.translation import get_language_from_path, ugettext as _

from app.models.personne import Personne
from app.views.common import LogTemporaire
from third_party.authomatic_0_1_0 import authomatic
from third_party.authomatic_0_1_0.authomatic import adapters
from third_party.authomatic_0_1_0.authomatic.providers import oauth1, oauth2, \
    openid, gaeopenid
from django.shortcuts import render, redirect

# (!!) beta testeur = message like
#      "please fill your profile, please..." + redirect to profile editing
SCRIPT_HIDE_AUTO = \
    "<script>$(document).ready(function() {\n" \
    "var hideAuto=function() {\n" \
    "    $('#btn-password').parent().closest('ul')" \
    "        .find('li').off('click', hideAuto);\n" \
    "    setTimeout(function(){ \n" \
    "        $('.panel-toggle-message').slideUp();\n" \
    "    }, 10000);\n" \
    "};\n" \
    "$('#btn-password').parent().closest('ul')" \
    ".find('li').on('click', hideAuto);\n" \
    "$($('#edit-profile-form').find('.row')[0]).show();\n" \
    "$('#profile-summary').hide();\n" \
    "});\n" \
    "</script>\n"

MESSAGE_BETA_TESTEUR = [
    _("Thank you for your registration and welcome aboard!"),
    _('<p style="margin-bottom: -34px;">Take a few clicks to fill out, '
      'confirm your practical information and continue the adventure.</p>'),
    SCRIPT_HIDE_AUTO,
    _('<p style="margin-bottom: -34px;">'
      '<b>Don’t forget that in order for Cogofly members to find and '
      'notice you via their different searches, you need to add '
      'your travel plans: trips, weekends and days out...</b></p>'),
    "<script>$(document).ready(function() { "
    "$('#profile-btn-edit').click();"
    "});</script>",
    _("Click here to hide this message")]

# Merci pour vous être enregistré est utilisé à plusieurs endroits :
MESSAGE_THANKS_FOR_REGISTER_CHANGE_PASSWORD = [
    _('Thanks for registering!'),
    _('You have been successfully registered.'),
    _('Please <strong>change your password</strong>.'),
    _('And then you can complete your profile.'),
    # Exemple d'image débile (que j'avais trouvée amusante mais pas Franck) :
    # u'<img id="fun" src="'+static('img/fun/thanks.gif')+u'" />',
    SCRIPT_HIDE_AUTO,
    "<script>$(document).ready(function() { "
    # Hack pour afficher l'onglet password :
    "$('#btn-password > a').click();"
    "});</script>",
    _('Click here to hide this message')]

# Create your views here.
CONFIG = {
    # ==========================================================================
    # Defaults
    # ==========================================================================

    '__defaults__': {
        # This is an optional special item where you can define
        # default values for all providers. You can override each default
        # value by specifying it in concrete provider dict.
        'sreg': ['Franck Lagathu', 'France'],
        'pape': [
            'https://schemas.openid.net/pape/policies/2007/06/multi-factor'
        ],
    },

    # ==========================================================================
    # OAuth 2.0
    # ==========================================================================

    'facebook': {
        'class_': oauth2.Facebook,  # Provider class. Don't miss the underscore!

        # Provider type specific keyword arguments:
        # Unique value used for serialization of credentials
        # only needed by OAuth 2.0 and OAuth 1.0a.
        'short_name': 1,
        #  Id de l'application :
        'consumer_key': '755565081236511',
        # Secret assigned to consumer by the provider:
        'consumer_secret': 'efe3cf28d4a83bc198d4df95d6ae48ec',
        # List of requested permissions only needed by OAuth 2.0:
        # https://developers.facebook.com/docs/facebook-login/permissions/v2.4#reference
        'scope': ['public_profile', 'email', 'user_friends']
    },
    'google': {
        # Can be a fully qualified string path:
        'class_': 'authomatic.providers.oauth2.Google',

        # Provider type specific keyword arguments:

        # use authomatic.short_name() to generate this automatically
        'short_name': 2,
        'consumer_key': '264525966015-orq8eiuh15eqsd7i79fo0106hvs0vo0r'
                        '.apps.googleusercontent.com',
        'consumer_secret': 'ZLPGIynNkZfm-YQzuRTKEm86',
        'scope': ['https://www.googleapis.com/auth/userinfo.profile',
                  'https://www.googleapis.com/auth/userinfo.email']
    },
    'windows_live': {
        # Can be a string path relative to the authomatic.providers module:
        'class_': 'oauth2.WindowsLive',

        # Provider type specific keyword arguments:
        'short_name': 3,
        'consumer_key': '###################',
        'consumer_secret': '###################',
        'scope': ['wl.basic',
                  'wl.emails',
                  'wl.photos']
    },

    # ==========================================================================
    # OAuth 1.0a
    # ==========================================================================

    'twitter': {
        'class_': oauth1.Twitter,

        # Provider type specific keyword arguments:
        'short_name': 4,
        'consumer_key': '###################',
        'consumer_secret': '###################'
        # OAuth 1.0a doesn't need scope.
    },

    # ==========================================================================
    # OpenID
    # ==========================================================================

    'oi': {
        'class_': openid.OpenID, # OpenID only needs this.
    },
    'gaeoi': {
        'class_': gaeopenid.GAEOpenID, # Google App Engine based OpenID provider.
    },
    'yahoo_oi': {
        'class_': openid.Yahoo,  # Predefined identifier 'https://me.yahoo.com'
        'sreg': ['email']  # Overrides the "sreg" defined in "__defaults__".
    },
    'google_oi': {
        'class_': openid.Google,  # OpenID provider with predefined identifier
    }
}
authomatic = authomatic.Authomatic(
    CONFIG,
    'TRL{`}A.T#NWPgex!z`L:%9uXf3#.WWcVf,\4`<[-NHZY<)gP8sq?HpC]fAf/v:4>WY7.a'
    'Q9PcB\?bXt7)*L5/A/J:"rEcTKSFWgs4euu_c%8,%8>fC#3&S^=E{\ZxWP8yW{,3BxS}N!'
)


def login(req, provider_name):

    def local_log_then_redirect(user_req, ex):

        def exception_infos():
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            return 'Exception in ({}, line {} "{}"): {}'.format(
                filename, lineno, line.strip(), exc_obj)

        LogTemporaire.write_log("An exception of type {} occured. ".format(
                                    type(ex).__name__))
        LogTemporaire.write_log('username = user_req.name = '
                                '{}'.format(user_req.name))
        LogTemporaire.write_log('email = user_req.email = '
                                '{}'.format(user_req.email))
        LogTemporaire.write_log('password = user_req.id = '
                                '{}'.format(user_req.id))
        EmailMessage(
            subject="An exception of type {} occured. ".format(
                        type(ex).__name__).encode('utf_8'),
            body='{}\n{}\n{}\n{}\n'.format(
                'username = user_req.name  = {}'.format(user_req.name),
                'email    = user_req.email = {}'.format(user_req.email),
                'password = user_req.id    = {}'.format(user_req.id),
                exception_infos()
            ).encode('utf_8'),
            from_email='contact@cogofly.com',
            to=['cogofly+error@gmail.com']).send()
        auth.logout(req)
        return HttpResponseRedirect(reverse('my_home_login'))

    def local_create_user(user_req):
        try:
            username = user_req.name
            loop = 0
            while User.objects.filter(username=username).count() > 0:
                loop += 1
                username = '{}_{}'.format(user_req.name, loop)

            retour = User.objects.create_user(
                username=username,
                email=user_req.email,
                password=user_req.id,
                last_name=user_req.last_name if user_req.last_name else '?',
                first_name=user_req.first_name if user_req.first_name else '?',
            )
            retour.save()

            if loop:
                EmailMessage(
                    subject=_('Login error: username already exists'),
                    body=_('He/she tried to login but '
                           'username was already taken, so we changed it to: '
                           '{}.\nHis/her email is: {}').format(
                        username, user_req.email
                    ),
                    from_email='contact@cogofly.com',
                    to=['cogofly+error@gmail.com', ],
                    bcc=[]).send()

        except IntegrityError as ex:   # column username is not unique
            req.session['message'] = [
                _('Technical error'),
                _("You tried to connect with Facebook or Google, but the "
                  "mail was already registered without Facebook or google."),
                _("Try to login by entering mail and password below, "
                  "without using Facebook or Google"),
                _('Click here to hide this message')]
            return local_log_then_redirect(user_req, ex)
        except User.DoesNotExist as ex:
            local_log_then_redirect(user_req, ex)
            req.session['message'] = [
                _('Technical error'),
                _("You tried to connect with Facebook or Google."),
                _("There was a technical error with Facebook or Google."),
                _("We're sorry for this."),
                _("Please try again to login."),
                _('Click here to hide this message')]
            return local_log_then_redirect(user_req, ex)

        # (!) memo JSON: .load() = from file, .loads() = parse string
        if user_req.content is not None:
            try:
                infos = json.loads(user_req.content)
            except ValueError:
                infos = None
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                LogTemporaire.write_log('BUG JSON !!')
                LogTemporaire.write_log(user_req.content)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            infos = None

        # (!) Reste à faire : analyser infos et écrire les champs dans Personne
        Personne.objects.create(
            user=retour,
            est_physique=True,
            champs_supplementaires=infos if infos is not None else '',
            one_click_login=True,
        )
        return retour

    # (!) moteur d'authentification custom :
    def local_authenticate(user_req):
        # (!) pas dans try-except :
        try:
            return auth.authenticate(email=user_req.email,
                                     secure='_.|._')
        except User.MultipleObjectsReturned as ex:
            return local_log_then_redirect(user_req, ex)
        # except User.DoesNotExist as exc:
        #    return local_log_then_redirect(user_req, exc)

    # Param GET url: si présent, on le met dans la session, pour faire un
    # redirect lorsque l'authentification aura fonctionné :
    url = req.GET.get('url', None)
    if url is not None:
        if req.session.get('url_back', None) is not None:
            del req.session['url_back']
            # param url n'est qu'une fois -> une seule fois par ici -> logout()
            auth.logout(req)

        # (!) resolve() utilisé pour deviner la langue en cours
        #     -> essayer de deviner, puis activer la langue avant resolve()
        lg_curr = translation.get_language()
        lg_url = get_language_from_path(url) or lg_curr
        translation.activate(lg_url)
        try:
            resolve(url)
            req.session['url_back'] = url  # pas d'erreur -> ok, URL connue
        except Resolver404:
            pass
        translation.activate(lg_curr)

        # Supprimer GET['url'] sinon ça ne plaît pas du tout à google d'avoir
        # des paramètres en plus au moment de l'authentification.
        # Hack : on ne peut pas supprimer des paramètres à moins de passer
        # par une copie : http://stackoverflow.com
        # /questions/18930234/django-modifying-the-request-object
        req.GET = req.GET.copy()
        del req.GET['url']

    response = HttpResponse()
    result = authomatic.login(adapters.DjangoAdapter(req, response),
                              provider_name)
    if result:
        # Récupérer la redirection pour ramener l'utilisateur où il était
        redirect = req.session.get('url_back', None)
        if redirect is None:
            redirect = req.GET.get('next')

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        LogTemporaire.write_log('redirect -> {}'.format(redirect))
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if result.error:
            auth.logout(req)
            response.write(
                '<h2>Erreur #1 : {}</h2>'.format(result.error.message)
            )

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            LogTemporaire.write_log('<h2>Erreur #2 : {}</h2>'.format(
                result.error.message))
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        elif result.user:
            user = result.user

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            LogTemporaire.write_log('user vaut quelque chose : {}'.format(
                str(user)))
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if not (user.name and user.id):
                result.user.update()
                user = result.user
            if not user.name and not user.id and not user.email \
                    and user.content:
                raise Exception(json.loads(user.content)['error'])
            elif not user.name:
                auth.logout(req)
                req.session['message'] = [
                    _('No name'),
                    _("You tried to connect but did'nt precise a name"),
                    _("We're sorry but we need at least an email and a name "
                      "to go further."),
                    _('Click here to hide this message')]
                return HttpResponseRedirect(reverse('my_home_error'))
            elif not user.id:
                auth.logout(req)
                raise Exception("Erreur d'authentification : aucun id")
            elif not user.email:
                auth.logout(req)
                req.session['message'] = [
                    _('No email'),
                    _("You tried to connect but did'nt precise an email"),
                    _("We're sorry but we need at least an email to "
                      "go further."),
                    _('Click here to hide this message')]
                return HttpResponseRedirect(reverse('my_home_error'))
                # raise Exception("Erreur d'authentification : aucun email")
            else:
                # we:
                # (1) authenticate
                # (2) if failure, create account then try to authenticate again
                # (3) if success (1) or (2) then call login():
                user_db = None
                try:
                    user_db = local_authenticate(user)

                    # ! Si l'utilisateur a été invité et qu'entretemps il se
                    #   connecte DIRECTEMENT, sans avoir cliqué sur le lien
                    #   d'invitation -> simuler une 1ère fois :
                    try:
                        if isinstance(user_db, (list, tuple)):
                            if len(user_db):
                                for u in user_db:
                                    LogTemporaire.write_log('USER IS A LIST!!')
                                    LogTemporaire.write_log(str(u))
                                user_db = user_db[0]
                        p = Personne.objects.get(user=user_db)
                    except TypeError as exc:
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        LogTemporaire.write_log('user:')
                        LogTemporaire.write_log(str(user))
                        LogTemporaire.write_log('user_db:')
                        LogTemporaire.write_log(str(user_db))
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        return local_log_then_redirect(user, exc)

                    if not p.user.is_active:  # Activer qu'une fois
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        LogTemporaire.write_log('? invité mais connect '
                                                'DIRECT !')
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        p.user.is_active = True
                        p.user.save()
                        p.confirmation_code = None
                        p.save()
                        req.session['message'] = [
                            _(msg) for msg in MESSAGE_BETA_TESTEUR]
                        # Simuler un reset password pour ne pas avoir le
                        # champ "old password"
                        req.session['reset_password'] = True
                        redirect = 'my_home_profile_edit'

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    LogTemporaire.write_log('local_authenticate() : {}'.format(
                        str(user_db)))
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    if redirect is not None:
                        try:
                            # Hack quand on vient directement de la page
                            # 'connexion' : si on a cliqué sur google ou
                            # facebook, la langue était perdue, alors j'ai
                            # sauvé le nom de l'url et la langue en cours :

                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            LogTemporaire.write_log('on entre dans le hack')
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                            if redirect.startswith('my_home_'):
                                langue = req.session.get('url_language',
                                                         None)
                                if langue:
                                    translation.activate(langue)
                                redirect = reverse(redirect)
                            else:
                                r = resolve(redirect)
                                if not r.view_name.startswith('my_home_'):
                                    redirect = None

                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            LogTemporaire.write_log('redirect : {}'.format(
                                redirect))
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                            if redirect:
                                auth.login(req, user_db)
                                return HttpResponseRedirect(redirect)

                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            LogTemporaire.write_log('on ne fait rien !')
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                        except Resolver404 as e:
                            print(redirect)
                            print(e)
                        else:
                            pass

                    # noter ça en session et dans le template afficher msg :

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    LogTemporaire.write_log('noter que "reg_already_done"')
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    req.session['reg_already_done'] = True
                    return HttpResponseRedirect(
                        reverse('my_home_index')
                    )
                except User.DoesNotExist:
                    result = local_create_user(user)
                    if result is not None:
                        if isinstance(result, HttpResponseRedirect):
                            return result
                        user_db = local_authenticate(user)
                        user_db.is_active = True
                        user_db.save()
                        p = Personne.objects.get(user=user_db)
                        # noter ça en session pour msg dans le template :
                        req.session['reg_validated'] = True

                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        LogTemporaire.write_log('new user : {}'.format(str(p)))
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                        # Hack presque copié-collé juste au dessus,
                        # cf commentaires au dessus sur 'redirect'
                        if redirect is None:
                            redirect = reverse('applancement_index')
                        elif redirect.startswith('my_home_'):
                            p.is_beta_tester = True
                            p.save()
                            langue = req.session.get('url_language', None)
                            if langue:
                                translation.activate(langue)
                            auth.login(req, user_db)
                            # (!!) création = message + redirect en dur :
                            req.session['message'] = [
                                _(msg) for msg in MESSAGE_BETA_TESTEUR]
                            # Simuler un reset password pour ne pas avoir le
                            # champ "old password"
                            req.session['reset_password'] = True

                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            LogTemporaire.write_log(
                                'redirect OK + MESSAGE_BETA_TESTEUR '
                                'my_home_profile_edit')
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                            return HttpResponseRedirect(
                                reverse('my_home_profile_edit'))
                        else:
                            lg_curr = translation.get_language()
                            lg_url = get_language_from_path(redirect) \
                                or lg_curr
                            translation.activate(lg_url)
                            r = resolve(redirect)
                            if r.view_name.startswith('my_home_'):
                                auth.login(req, user_db)
                                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                LogTemporaire.write_log(
                                    'redirect 222 vers {}'.format(r.view_name))
                                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            else:
                                redirect = 'applancement_index'

                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        LogTemporaire.write_log(
                            'au final, redirect = {}'.format(redirect))
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                        return HttpResponseRedirect(redirect)

                if user_db is not None:
                    response.write('<h1>Found : {}</h1>'.format(user_db))
                    if user_db.is_active:
                        # ok, valider que l'utilisateur est bien connecté :
                        auth.login(req, user_db)
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        LogTemporaire.write_log(
                            'redirect PAS beta : {}'.format(redirect or '/'))
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        return HttpResponseRedirect(redirect or '/')
                    else:
                        response.write('Compte désactivé')
        else:  # User is none -> aucune authentification
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            LogTemporaire.write_log(
                'User is none -> aucune authentification ! WTF')
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return HttpResponseRedirect(redirect or '/')
    return response


def logout(req):
    auth.logout(req)
    url = req.GET.get('url', None)
    if url is not None:
        lg_curr = translation.get_language()
        # Voir commentaire au dessus du même code de 4 lignes :
        lg_url = get_language_from_path(url) or lg_curr
        translation.activate(lg_url)
        try:
            resolve(url)
            redirect = url
        except Resolver404:
            redirect = '/'
        translation.activate(lg_curr)
        return HttpResponseRedirect(redirect)
    return HttpResponseRedirect('/')


#new functions 

def addtrip(request):
    return render(request, 'my_home/addtrip.html')

def tripcard(request):
    return render(request, 'my_home/tripcard.html')

def profile(request):
    return render(request, 'my_home/profile.html')

def review(request):
    return render(request, 'my_home/review.html')

def tripsdone(request):
    return render(request, 'my_home/tripsdone.html')
    
def demo(request):
    return render(request, 'my_home/demo.html')