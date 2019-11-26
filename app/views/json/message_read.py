# coding=UTF-8


from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import generic

from app.models.conversation import Message
from app.models.personne import Personne
from app.views.common import LoginRequiredMixin


class JsonMessageReadView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        try:
            a = Message.objects.get(pk=int(kwargs['id_message']))
        except ValueError:  # erreur conversion = hack:
            return redirect('my_home_index')

        p = Personne.objects.get(user=request.user)
        # on ne peut marquer lu qu'un message dont on est le destinataire :
        if a.dst != p:
            return redirect('my_home_index')
        a.is_read = True
        a.save()
        return JsonResponse({'message': '', 'success': True})


