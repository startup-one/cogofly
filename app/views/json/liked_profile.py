# coding=UTF-8


from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from django.views import generic
from django.utils.datetime_safe import datetime as django_datetime

from app.models.personne import PersonneLiked, Personne
from app.views.common import LoginRequiredMixin


class JsonLikedProfileView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        try:
            # print(u'json liked... id_profile = {}'.format(
            #    int(kwargs['id_profile'])))
            liked = True
            p_liked = Personne.objects.get(pk=int(kwargs['id_profile']))
        except ValueError:  # hack:
            return redirect('my_home_index')
        p = Personne.objects.get(user=request.user)
        # !! Si on a déjà "liké", le mettre à False :
        deja_fait = PersonneLiked.objects.filter(src=p, dst=p_liked,
                                                 date_v_fin__isnull=True)
        if len(deja_fait):
            if deja_fait[0].liked:
                liked = False
            # print(u'-> updating, liked est : {}'.format(liked))
            deja_fait.update(date_v_fin=make_aware(django_datetime.now()))

        obj = PersonneLiked.objects.create(src=p, dst=p_liked, liked=liked)
        obj.save()
        # print(u'json ok !')
        return JsonResponse({'message': '', 'success': True, 'liked': liked})


