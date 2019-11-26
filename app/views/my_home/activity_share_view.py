# coding=UTF-8

from copy import deepcopy

import pytz
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime
from django.utils.timezone import now
from django.views import generic

from app.models.personne import Activite, Personne, ActiviteShared
from app.views.common import LoginRequiredMixin, CommonView
from cogofly.settings import TIME_ZONE


class ActivityShareView(LoginRequiredMixin, generic.TemplateView):
    """
    Vue utilisée par la page principale pour partager une activité avec
    ses contacts
    """

    def get_context_data(self, **kwargs):
        context = super(ActivityShareView, self).get_context_data(**kwargs)
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']
        return context

    def post(self, request):
        common = CommonView(self)
        # Astuce : dupliquer un enregistrement complet = le chercher + pk=None
        # http://stackoverflow.com/questions/4733609/
        # how-do-i-clone-a-django-model-instance-object-and-save-it-to-the-database
        try:
            activite = Activite.objects.get(pk=int(request.POST['activite']))
        except ValueError:
            return redirect('my_home_index')  # hack -> juste redirect

        personne = common.infos['personne']

        # Chercher les pk des personnes pour qui on a déjà partagé l'activité :
        deja_shared = set(ActiviteShared.objects.filter(activite=activite)
                          .values_list('dst__pk', flat=True))
        contacts_pks = set([p.pk for p in personne.contacts])
        for v in request.POST.getlist('contacts[]'):
            try:
                if v == 'on':  # c'était la case "tout cocher" -> ignorer
                    continue
                v = int(v)
                if v not in contacts_pks:  # hack
                    return redirect('my_home_index')
                if v in deja_shared:  # déjà partagé
                    continue
                a_s = ActiviteShared.objects.create(
                    src=personne,
                    dst=Personne.objects.get(pk=v),
                    activite=activite
                )
                a_s.save()
            except ValueError:  # hack
                return redirect('my_home_index')
        return redirect('my_home_index')


