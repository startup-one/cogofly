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


class LanguageView(generic.TemplateView):
    template_name = 'my_home/language.html'

    def get_context_data(self, **kwargs):
        common = CommonView(self, **kwargs)
        context = super(LanguageView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('Language')
        return context


