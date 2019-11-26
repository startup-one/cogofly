# coding=UTF-8


from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from django.views import generic
from django.utils.datetime_safe import datetime as django_datetime

from app.models.personne import Activite, PersonneLiked, Personne
from app.views.common import LoginRequiredMixin


class JsonLikedReadView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        try:
            a = PersonneLiked.objects.get(pk=int(kwargs['id_personne_like']))
        except ValueError:  # erreur conversion = hack:
            return redirect('my_home_index')
        p = Personne.objects.get(user=request.user)
        if a.dst != p:  # hack: on a envoyé un id PersonneLiked à la main
            return redirect('my_home_index')
        a.viewed = True
        a.save()
        return JsonResponse({'message': '', 'success': True})


