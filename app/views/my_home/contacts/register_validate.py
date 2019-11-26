# coding=UTF-8


from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from app.models.personne import Personne, Activite, PersonneRelation
from applancement.views.views import MESSAGE_BETA_TESTEUR, \
    MESSAGE_THANKS_FOR_REGISTER_CHANGE_PASSWORD


class RegisterValidateView(TemplateView):
    # Variables écrasées par les descendants (cf commentaire dans descendants) :
    message = MESSAGE_BETA_TESTEUR
    reset_password = False

    def get(self, request, *args, **kwargs):
        rand_str = kwargs['rand_str']
        try:
            p = Personne.objects.get(confirmation_code__exact=rand_str)
            user = auth.authenticate(username=p.user.username,
                                     password=p.temporary_visible_password)
            if user is not None:
                auth.login(request, user)
                if not p.user.is_active:  # Activer qu'une fois
                    p.user.is_active = True
                    p.user.save()
                    p.confirmation_code = None
                    p.save()
                    self.request.session['message'] = [
                        _(msg) for msg in self.message]
                    # Ajouter au mur deux fois
                    r = PersonneRelation.objects.filter(dst=p).all()
                    if len(r) == 1:  # Devrait toujours être le cas
                        r = r[0]
                        m = Activite(activite=Activite.ACTIVITE_AJOUT_RELATION,
                                     relation=r)
                        m.save()
                        m = Activite(activite=Activite.ACTIVITE_AJOUT_RELATION,
                                     relation=r.opposite)
                        m.save()

                    # Surchargé par le descendant qui le met à True car
                    # le descendant = vue affichée quand on est invité = forcer
                    # à faire un reset password
                    self.request.session['reset_password'] = self.reset_password
        except Personne.DoesNotExist:
            pass

        # Que ça ait fonctionné ou pas, redirect sur l'édition du profil
        # -> s'il ne s'est pas identifié -> "re"-redirect vers la page de login
        return HttpResponseRedirect(reverse('my_home_profile_edit'))


class ContactRegisterValidateView(RegisterValidateView):
    # 3 vues de confirmation possible :
    # - on s'inscrit = entrer un mot de passe -> lien par mail -> vue ici
    # - on s'inscrit = entrer un mot de passe -> lien par mail -> vue ici
    # le lien de validation "changer mot de passe" ou "confirmer enregistrement"
    # forcer à faire un reset password
    # Il n'y a qu'ici qu'il faut demander à changer le mot de passe :
    message = MESSAGE_THANKS_FOR_REGISTER_CHANGE_PASSWORD
    reset_password = True
