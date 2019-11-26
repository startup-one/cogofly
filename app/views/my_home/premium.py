# coding=UTF-8


from django.contrib import auth
from django.urls import reverse_lazy, resolve, Resolver404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.message_send import MessageSendForm
from app.models.personne import Personne, PersonneRelation, Activite, \
    PersonneLiked
from app.views.common import CommonView
from app.views.my_home.post_message_view import PostMessageView


class PremiumView(generic.TemplateView):
    template_name = 'my_home/premium.html'

    def get_context_data(self, **kwargs):
        context = super(PremiumView, self).get_context_data(**kwargs)
        common = CommonView(self)
        context['common'] = common.infos
        return context

