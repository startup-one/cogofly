# coding=UTF-8



from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from django.views import generic
from django.utils.datetime_safe import datetime as django_datetime

from app.models.personne import Activite, PersonneLiked, Personne
from app.views.common import LoginRequiredMixin


class JsonLikedView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        try:
            print(('json liked... id_activite = {}'.format(
                int(kwargs['id_activite']))))
            liked = True
            a = Activite.objects.get(pk=int(kwargs['id_activite']))
        except ValueError:  # hack:
            return redirect('my_home_index')
        p = Personne.objects.get(user=request.user)
        if a.travel:
            dst = a.travel.personne
        elif a.express_yourself:
            dst = a.express_yourself.personne
        else:
            dst = a.relation.src
        # !! Si on a déjà "liké", le mettre à False :
        deja_fait = PersonneLiked.objects.filter(src=p, dst=dst, activite=a,
                                                 date_v_fin__isnull=True)
        if len(deja_fait):
            if deja_fait[0].liked:
                liked = False
            print(('-> updating, liked est : {}'.format(liked)))
            deja_fait.update(date_v_fin=make_aware(django_datetime.now()))

        obj = PersonneLiked.objects.create(src=p, dst=dst, activite=a,
                                           liked=liked)
        obj.save()
        print('json ok !')
        return JsonResponse({'message': '', 'success': True, 'liked': liked})

    # def post(self, request, *args, **kwargs):
    #     # exemple pour gérer le post, mais je n'ai pas le temps, je le fais
    #     # en get pour l'instant :
    #     # c = csrf(request)
    #     # print(c['csrf_token'])
    #     # return JsonResponse({'csrf_token': str(c['csrf_token'])})
    #     return redirect('my_home_index')


