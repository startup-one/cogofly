# coding=UTF-8


from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from app.models.personne import Personne, Activite, PersonneRelation
from applancement.views.views import MESSAGE_BETA_TESTEUR, \
    MESSAGE_THANKS_FOR_REGISTER_CHANGE_PASSWORD


class AccountReactivateView(TemplateView):
    # Variables écrasées par les descendants (cf commentaire dans descendants) :
    message = MESSAGE_BETA_TESTEUR
    reset_password = False

    def get(self, request, *args, **kwargs):
        rand_str = kwargs['rand_str']
        try:
            p = Personne.objects.get(reactivate_code__exact=rand_str)
            p.est_active = True
            p.reactivate_code = None
            p.save()
            # obligatoire de faire un authenticate avant login,
            # authentification faible avec mot de passe en dur :
            user = auth.authenticate(email=p.user.email, secure='_.|._')
            auth.login(request, user)
            self.request.session['message'] = [
                _('Welcome back!'),
                _('Your account has been successfully reactivated'),
                _('Click here to hide this message')]
        except Personne.DoesNotExist:
            return redirect('app_index')

        return HttpResponseRedirect(reverse('my_home_profile_edit'))


