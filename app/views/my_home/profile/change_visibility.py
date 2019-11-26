# coding=UTF-8


from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.profile.profile_visibilite import ProfileVisibiliteForm
from app.models.personne import Personne
from app.models.personne_enums import PersonneEnums
from app.views.common import LoginRequiredMixin


class ChangeVisibilityView(LoginRequiredMixin, generic.FormView):
    template_name = 'my_home/profile/base.html'
    form_class = ProfileVisibiliteForm
    success_url = reverse_lazy('my_home_profile_edit')

    def get(self, request, *args, **kwargs):
        retour = super(ChangeVisibilityView, self).get(request, *args, **kwargs)
        # (!) il ne calcule la vue que si nécessaire !
        # -> forcer à le faire *AVANT* de supprimer le message :
        retour.render()
        if self.request.session.get('message', None):
            del self.request.session['message']
        return retour

    def get_object(self):
        p = Personne.objects.filter(
            user__pk__exact=self.request.user.pk
        ).all()
        return p[0] if len(p) else None

    def form_valid(self, form):
        def local_bool(idx):
            return True if form.cleaned_data.get(idx, False) else False

        p = self.get_object()
        p.niveau_visibilite = form.cleaned_data.get(
            'niveau_visibilite', PersonneEnums.VISIBILITE_TOUT_LE_MONDE)
        p.age_visible = local_bool('age_visible')
        p.nb_enfants_visible = local_bool('nb_enfants_visible')
        p.langue_visible = local_bool('langue_visible')
        p.langues2_visible = local_bool('langues2_visible')
        p.niveau_etudes_visible = local_bool('niveau_etudes_visible')
        p.programme_visible = local_bool('programme_visible')
        p.employer_current_visible = local_bool('employer_current_visible')
        p.employer_previous_visible = local_bool('employer_previous_visible')
        p.profession_visible = local_bool('profession_visible')
        p.activite_visible = local_bool('activite_visible')
        p.hobbies_visible = local_bool('hobbies_visible')
        p.conduite_visible = local_bool('conduite_visible')
        p.personnalite_visible = local_bool('personnalite_visible')
        p.est_fumeur_visible = local_bool('est_fumeur_visible')
        p.custom_zodiac_sign_visible = local_bool('custom_zodiac_sign_visible')
        p.self_description_visible = local_bool('self_description_visible')
        p.save()

        # Exemple de gestion d'erreur, mais ici c'est toujours ok :
        error = None
        if not error:
            # !! RESTE A FAIRE : mettre à jour le mot de passe
            self.request.session['message'] = (
                _("Account updated"),
                _("Your visibility configuration has been changed."))
        else:
            self.request.session['message'] = (
                _("Your visibility configuration has not been changed:"
                  "<br/><br/>{}").format(error),
                _("Please try again"))

        return super(ChangeVisibilityView, self).form_valid(form)
#
