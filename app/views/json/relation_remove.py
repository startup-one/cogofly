# coding=UTF-8


from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views import generic

from app.models.personne import Personne, PersonneRelation
from app.models.personne_enums import PersonneEnums
from app.views.common import LoginRequiredMixin


class JsonRelationRemoveView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        try:
            dst_pk = int(kwargs['id_personne'])
        except ValueError:  # hack
            return redirect('my_home_index')

        # Création de la relation "invitation" :
        p_cur = Personne.objects.get(user=request.user)
        p_dst = Personne.objects.get(pk=dst_pk)
        prs1 = PersonneRelation.objects.filter(src=p_cur, dst=p_dst)
        prs2 = PersonneRelation.objects.filter(dst=p_cur, src=p_dst)
        if (not len(prs1)) or (not len(prs2)):
            return redirect('my_home_index')
        prs1.update(type_relation=PersonneEnums.RELATION_RETIREE)
        prs2.update(type_relation=PersonneEnums.RELATION_RETIREE)

        self.request.session['message'] = [
            _("The relationship with {} has been removed").format(
                p_dst.full_name()),
            _("Click here to hide this message")]
        return JsonResponse({'message': '', 'success': True})

    # def post(self, request, *args, **kwargs):
    #     # exemple pour gérer le post, mais je n'ai pas le temps, je le fais
    #     # en get pour l'instant :
    #     # c = csrf(request)
    #     # print(c['csrf_token'])
    #     # return JsonResponse({'csrf_token': str(c['csrf_token'])})
    #     return redirect('my_home_index')


