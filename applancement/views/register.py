# coding=UTF-8


import uuid

from datetime import datetime

import pytz
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView

from app.forms.forms import RegisterForm
from app.models.personne import Personne
from applancement.views.views import MESSAGE_BETA_TESTEUR
from cogofly.settings import TIME_ZONE


class RegisterView(FormView):
    template_name = 'applancement/index.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['agree_with_toc_and_tos'] = \
            _("By clicking the Sign Up button, you agree to our "
              "<a href=\"{0}\" target=\"_blank\">Terms &amp; Conditions</a> "
              "and confirm that you have read our "
              "<a href=\"{1}\" target=\"_blank\">Data Usage Policy</a>, "
              "including our use of Cookies, mobile app, and APIs "
              "(Facebook, Twitter, Google+, LinkedIn, etc.).")\
            .format(
                reverse('terms_and_conditions'),
                reverse('terms_of_service')
            )
        return context

    def get(self, request, *args, **kwargs):
        retour = super(RegisterView, self).get(request, *args, **kwargs)
        # (!) il ne calcule la vue que si nécessaire !
        # -> forcer à le faire *AVANT* de faire les "logout()" :
        retour.render()
        # Ce qui suit = lorsque l'utilisateur a fait une action, je l'ai
        # enregistré dans la session et j'ai fait un redirect afin de ne
        # lui afficher qu'un seul message
        if self.request.session.get('reg_done_check_email', None):
            del request.session['reg_done_check_email']
        if self.request.session.get('reg_validated', None):
            del request.session['reg_validated']
            auth.logout(request)
        if self.request.session.get('reg_already_done', None):
            del request.session['reg_already_done']
            auth.logout(request)

        return retour

    def form_valid(self, form):
        # username = form.cleaned_data['username']
        prenom = form.cleaned_data['prenom']
        nom = form.cleaned_data['nom']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 != password2:
            form.add_error('password2', _('Passwords do not match'))
            return super(RegisterView, self).form_invalid(form)

        # hack pour faire un fake username
        username = email.replace('@', '_at_')
        # Si username déjà utilisé, erreur :
        if len(User.objects.filter(username__exact=username)):
            err = _('A user has already the same firstname and lastname')
            form.add_error('prenom', err)
            form.add_error('nom', err)
            return super(RegisterView, self).form_invalid(form)
        # Si email déjà utilisé, erreur :
        if len(User.objects.filter(email__exact=email)):
            form.add_error('email', _('This email is already used'))
            return super(RegisterView, self).form_invalid(form)

        # Création de l'utilisateur :
        user = User.objects.create_user(username=username, email=email,
                                        password=password1,
                                        first_name=prenom, last_name=nom)
        user.is_active = False
        user.save()
        rand_str = str(uuid.uuid4())
        p = Personne(user=user, confirmation_code=rand_str,
                     champs_supplementaires='')
        p.save()

        site_web = "{}://{}".format(
            self.request.scheme, self.request.META['HTTP_HOST']
        )
        if 'development' not in self.request.META['HTTP_HOST']:
            EmailMessage(
                subject=_('Thanks for registering!').encode('utf_8'),
                body='{}\n{}\n{}\n{}{}'.format(
                    _("Thanks again for signing up."),
                    _("We sincerely hope that you will appreciate this "
                      "new and innovative international social network, "
                      "for which the operative word is “sharing”"),
                    _("To validate your registration, "
                      "click on the following link:"),
                    site_web,
                    reverse('register_validate', kwargs={'rand_str': rand_str})
                ).encode('utf_8'),
                from_email='register@cogofly.com',
                to=[form.cleaned_data['email']],
                # bcc=[u'cogofly@gmail.com'],
                ).send()

        self.request.session['reg_done_check_email'] = True
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


class RegisterValidateView(TemplateView):
    template_name = 'applancement/index.html'

    def get(self, request, *args, **kwargs):
        rand_str = kwargs['rand_str']
        try:
            p = Personne.objects.get(confirmation_code__exact=rand_str)
        except Personne.DoesNotExist:
            p = None
        if p:
            if p.user.is_active:
                # Déjà actif ?
                # -> on a re-cliqué sur lien d'activation ou
                # -> on a demandé un reset du mot de passe
                if p.reset_password:
                    tz_ici = pytz.timezone(TIME_ZONE)
                    nb = p.reset_password.replace(tzinfo=tz_ici)
                    nb = (datetime.now(tz_ici) - nb).total_seconds()
                    if nb < 3600:
                        # Tricher via mon authentification qui ne nécessite
                        # pas de mot de passe :
                        user = auth.authenticate(username=p.user.username,
                                                 secure='_.|._')
                        if user is None:
                            user = auth.authenticate(email=p.user.email,
                                                     secure='_.|._')
                        if user is not None:
                            auth.login(request, user)
                            request.session['message'] = [
                                _("Password reset"),
                                # utiliser format pour qu'il n'y ait qu'une
                                # phrase (sinon je mets un <br/> inutile)
                                '{}{}'.format(
                                    _("<b>Please change your password</b>"),
                                    "<script>"
                                    "$(document).ready(function() { "
                                    "$('#profile-summary').hide();\n"
                                    "$('#my-parameters').show();\n"
                                    "$('#my-parameters-tab').hide();\n"
                                    "$('#btn-password > a').click();\n"
                                    " });"
                                    "</script>"
                                ),
                                _("Click here to hide this message")]
                            request.session['reset_password'] = True
                            return HttpResponseRedirect(
                                reverse('my_home_profile_edit'))

                    # Arrivé ici = tentative de reset mais... trop tard !
                    auth.logout(request)
                    request.session['message'] = [
                        _("Request refused"),
                        _("Password reset is valid for one hour"),
                        _("Please try again"),
                        _("Click here to hide this message")]
                else:
                    # Si pas reset password = re-cliqué sur lien d'activation
                    auth.logout(request)
                    request.session['message'] = [
                        _("Already done"),
                        _("You have already activated this account"),
                        _("Please log-in"),
                        _("Click here to hide this message")]
                # Dans tous les cas logout
                # Retour edit : si on est pas loggué, renvoi auto vers login :
                return HttpResponseRedirect(reverse('my_home_profile_edit'))
            else:
                p.user.is_active = True
                p.user.save()
                if p.is_beta_tester:
                    # obligatoire de faire un authenticate avant login,
                    # donc comme on n'a pas de mot de passe, je me sers de mon
                    # authentification faible avec mot de passe en dur :
                    user = auth.authenticate(email=p.user.email,
                                             secure='_.|._')
                    auth.login(request, user)
                    # (!!) beta testeur = message + redirect vers l'édition
                    self.request.session['message'] = [
                        _(msg) for msg in MESSAGE_BETA_TESTEUR]
                    return HttpResponseRedirect(reverse('my_home_profile_edit'))
                else:
                    # Mettre reg_validated dans la session, ce qui affichera
                    # un beau message "merci de vous être enregistré"
                    # et une seule fois
                    self.request.session['reg_validated'] = True

                return HttpResponseRedirect(reverse('applancement_index'))

        return super(RegisterValidateView, self).get(request, *args, **kwargs)

