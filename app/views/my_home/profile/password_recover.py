# coding=UTF-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms import ProfilePasswordRecoverForm
from app.models.personne import Personne


class PasswordRecoverView(generic.FormView):
    template_name = 'my_home/password_recover.html'
    form_class = ProfilePasswordRecoverForm
    success_url = reverse_lazy('my_home_login')

    def get(self, request, *args, **kwargs):
        retour = super(PasswordRecoverView, self).get(request, *args, **kwargs)
        # (!) il ne calcule la vue que si nécessaire !
        # -> forcer à le faire *AVANT* de supprimer le message :
        retour.render()
        if self.request.session.get('message', None):
            del self.request.session['message']
        return retour

    def form_valid(self, form):
        i_agree = form.cleaned_data.get('i_agree')
        email = form.cleaned_data.get('email')
        message = [_('No action!')]
        if i_agree and email:
            try:
                u = User.objects.get(email=email)
                p = Personne.objects.get(user=u)

                # si pas exception, c'est que trouvé -> ok :
                p.reset_password = datetime.datetime.now()
                rand_str = str(uuid.uuid4())
                p.confirmation_code = rand_str
                p.save()

                # (!) presque copié collé de my_home/register.py, centraliser
                #     toutes les méthodes, par exemple dans backends.py
                site_web = "{}://{}".format(
                    self.request.scheme, self.request.META['HTTP_HOST']
                )
                if 'development' not in self.request.META['HTTP_HOST']:
                    EmailMessage(
                        _('Password reset'),
                        _("You've asked to reset your password, "
                          "click on the following link:\n{}{}").format(
                              site_web,
                              reverse('register_validate',
                                      kwargs={'rand_str': rand_str})),
                        'register@cogofly.com',
                        [email],
                        # [u'cogofly+register@gmail.com'],
                        ).send()
            except (User.DoesNotExist, Personne.DoesNotExist):
                pass
            message = [
                _('Mail sent'),
                _("If the mail you've provided exists, "
                  "you should get a message with a link "
                  "to recover your password "
                  "in the few minutes to come.")]
        elif not email:
            message.append(_('No email provided'))
        else:
            message.append(
                _('If you want to get an email to recover your password, '
                  'please check "Yes".'))

        message.append(_('Click here to hide this message'))
        self.request.session['message'] = message
        return super(PasswordRecoverView, self).form_valid(form)
