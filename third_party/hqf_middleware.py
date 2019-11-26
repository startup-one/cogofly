# coding=UTF-8
# https://gist.github.com/vstoykov/1366794

from django.urls import resolve, Resolver404
from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from app.models.generic import Langue
from app.models.personne import Personne
from cogofly import settings


class RedirectIfUserIsNotActiveMiddleware(object):
    """
    Middleware pour rediriger si compte désactivé
    """
    @staticmethod
    def process_request(request):
        # passer par "Personne" = modèle de l'application = pas évolutif...
        # mais pas le choix, je n'arrive pas à trouver une solution élégante :
        try:
            p = Personne.objects.get(user__pk=request.user.pk)
            try:
                a = resolve(request.path)
                if a.app_name == 'admin':
                    return
                r = None
                if not p.est_active:  # Compte désactivé
                    r = settings.URL_REDIRECT_USER_NOT_ACTIVE
                if p.est_detruit:
                    r = settings.URL_REDIRECT_USER_DELETED
                if r:
                    # ne rien faire si on essaie d'aller sur ces URLS :
                    # - page "user not active"
                    # - page "user deleted"
                    # - fichiers statiques
                    # - page de réactivation
                    # - page déconnexion
                    # - page support (pour pouvoir écrire au support)
                    # - page erreur critique
                    if a.url_name not in [settings.URL_REDIRECT_USER_NOT_ACTIVE,
                                          settings.URL_REDIRECT_USER_DELETED,
                                          'url_public',
                                          'my_home_profile_account_reactivate',
                                          'my_home_logout',
                                          'my_home_remarks_and_testimonies',
                                          'my_home_error', ]:
                        return redirect(r)

            # request.path fait une 404 si URL pas connue -> ne rien faire :
            except Resolver404:
                pass
        except (Personne.DoesNotExist, TypeError):
            pass


class RedirectIfUserProfilNotCompleteMiddleware(object):
    """
    Middleware pour rediriger si profil pas entièrement complété
    """
    @staticmethod
    def process_request(request):
        # passer par "Personne" = modèle de l'application = pas évolutif...
        # mais pas le choix, je n'arrive pas à trouver une solution élégante :
        try:
            p = Personne.objects.get(user__pk=request.user.pk)
            try:
                a = resolve(request.path)
                if a.app_name == 'admin':
                    return
                if p.est_detruit or not p.est_active:  # détruit / désactivé
                    return

                # vérifier les champs obligatoires bien remplis :
                # (!) champs codés en dur ici :
                if p.profile_complete():
                    return

                # -> pas tous les champs remplis
                if a.url_name not in [
                   settings.URL_REDIRECT_USER_PROFILE_NOT_COMPLETE,
                   'url_public',
                   'my_home_error',
                   'my_home_profile_edit',
                   'my_home_logout',
                   'my_home_remarks_and_testimonies']:
                        return redirect(
                            settings.URL_REDIRECT_USER_PROFILE_NOT_COMPLETE)

            # request.path fait une 404 si URL pas connue -> ne rien faire :
            except Resolver404:
                pass
        except Personne.DoesNotExist:
            pass


class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions
    or cookies

    Should be installed *before* any middleware that checks
    request.META['HTTP_ACCEPT_LANGUAGE'], namely
    django.middleware.locale.LocaleMiddleware
    """
    @staticmethod
    def process_request(request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            if '/admin' not in request.path:
                del request.META['HTTP_ACCEPT_LANGUAGE']


class CheckIfLanguageChangedMiddleware(object):
    """
    Middleware pour vérifier si on a changé de langue ou pas. Cela sert pour
    les batches, pour envoyer selon la langue sélectionnée.
    """
    @staticmethod
    def process_request(request):
        try:
            p = Personne.objects.get(user__pk=request.user.pk)
            langue = translation.get_language()
            site_web = "{}://{}".format(
                request.scheme, request.META['HTTP_HOST']
            )
            if not p.site_web or p.site_web != site_web:
                p.site_web = site_web
                p.save()
            if not p.site_language or p.site_language.locale != langue:
                try:
                    p.site_language = Langue.objects.get(locale__exact=langue)
                    p.save()
                except Langue.DoesNotExist:
                    translation.activate('en')
                    request.session['message'] = [
                        str(_("Language unknown")),
                        str(_("The language you've set is unknown ('{}'). "
                              "Please go to My Profile -> Change my "
                              "parameters and choose a known language")
                            ).format(translation.get_language()),
                        str(_('Click here to hide this message')), ]
                    return redirect('page_not_found')

        except Personne.DoesNotExist:
            pass

