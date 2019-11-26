# coding=UTF-8


from django.db.models import Q, Max
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.comment_send import CommentSendForm
from app.forms.message_send import MessageSendForm
from app.models.personne import Personne, PersonneRelation, Activite, \
    PersonneLiked, ActiviteComments, ActiviteShared
from app.models.personne_enums import PersonneEnums
from app.views.common import CommonView
from app.views.my_home.post_message_view import PostMessageView


class ErrorView(generic.TemplateView):
    template_name = 'my_home/error.html'

    def get_context_data(self, **kwargs):
        common = CommonView(self)
        context = super(ErrorView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('Error')
        # Message éventuel à afficher :
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

