# coding=UTF-8


from django.db.models import Q
from django.shortcuts import redirect
from django.views import generic

from app.models.conversation import Conversation
from app.models.personne import Personne
from app.views.common import LoginRequiredMixin


class ConversationDeleteView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'my_home/notifications/base.html'

    def get(self, request, *args, **kwargs):
        return redirect('my_home_notifications')

    def post(self, request, *args, **kwargs):
        try:
            c = Conversation.objects.get(pk=int(kwargs['id_conversation']))
            p = Personne.objects.get(user=request.user)
            if len(c.messages.filter(Q(src=p) | Q(dst=p))):
                c.messages.filter(src=p).update(src_visible=False)
                c.messages.filter(dst=p).update(dst_visible=False, is_read=True)
        except ValueError:  # erreur conversion = hack:
            pass

        return redirect('my_home_notifications')


