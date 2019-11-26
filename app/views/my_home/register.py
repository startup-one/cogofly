# coding=UTF-8


import uuid

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.utils import translation
from django.views import generic
from django.utils.translation import ugettext as _

from app.forms.forms import RegisterForm
from app.models.personne import Personne
from app.views.common import CommonView


class RegisterView(generic.FormView):
    """
    Presque entièrement copié collé de "applancement.register.py"
    """
    template_name = 'my_home/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('my_home_index')

    def get_context_data(self, **kwargs):
        common = CommonView(self)
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
        context['common'] = common.infos
        context['titre'] = _('Sign up')
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def get(self, req, *args, **kwargs):
        retour = super(RegisterView, self).get(req, *args, **kwargs)
        # (!) il ne calcule la vue que si nécessaire !
        # -> forcer à le faire *AVANT* de faire les "logout()" :
        retour.render()
        # Ce qui suit = lorsque l'utilisateur a fait une action, je l'ai
        # enregistré dans la session et j'ai fait un redirect afin de ne
        # lui afficher qu'une seule fois le message ()
        if req.session.get('force_logout', None):
            del req.session['force_logout']
            auth.logout(req)

        # si on se connecte via google ou facebook, url_back est utilisée :
        req.session['url_back'] = 'my_home_index'
        # (!) si via google ou facebook il oublie la langue en cours !
        req.session['url_language'] = translation.get_language()
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
        try:
            user = User.objects.create_user(username=username, email=email,
                                            password=password1,
                                            first_name=prenom, last_name=nom)
        except IntegrityError:
            form.add_error('username', _('This username is already used'))
            return super(RegisterView, self).form_invalid(form)

        user.is_active = False
        user.save()
        rand_str = str(uuid.uuid4())
        p = Personne(user=user, confirmation_code=rand_str,
                     champs_supplementaires='',
                     # Si on s'enregistre ici = beta testeur
                     is_beta_tester=True)
        p.save()

        site_web = "{}://{}".format(
            self.request.scheme, self.request.META['HTTP_HOST']
        )
        if 'development' not in self.request.META['HTTP_HOST']:
            EmailMessage(
                subject=_('Thanks again for signing up.'),
                body=_('We sincerely hope that you will appreciate this new '
                       'and innovative international social network, '
                       'for which the operative word is “sharing”\n'
                       "To validate your registration, "
                       "click on the following link:\n{}{}").format(
                           site_web,
                           reverse('register_validate',
                                   kwargs={'rand_str': rand_str})),
                from_email='register@cogofly.com',
                to=[form.cleaned_data['email']],
                bcc=['cogofly@gmail.com']).send()

        self.request.session['message'] = [
            _('Thanks for signing up!'),
            _('An email confirmation has been sent to you.'),
            _('Please check your mailbox in order to activate your account, '
              'via the link provided, and start the adventure!'),
            _('Click here to hide this message')]
        return super(RegisterView, self).form_valid(form)

