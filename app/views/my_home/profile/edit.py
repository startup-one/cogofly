# coding=UTF-8

import copy

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.datetime_safe import datetime as django_datetime
from django.utils.timezone import make_aware
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.profile.profile import ProfileForm
from app.forms.profile.profile_delete import ProfileDeleteForm
from app.forms.profile.profile_desactivate import ProfileDesactivateForm
from app.forms.profile.profile_newsletter_configuration import \
    ProfileNewsletterConfigurationForm
from app.forms.profile.profile_password import ProfilePasswordForm
from app.forms.profile.profile_visibilite import ProfileVisibiliteForm
from app.models.generic import PictureURL
from app.models.publicite import Publicite
from app.models.tag import TagTraduit, TagBase
from app.models.personne import Photo, Personne, PersonnePhoto, PersonneHobby, \
    PersonneProgramme, PersonneActivite, PersonneTypepermis, \
    PersonnePersonnalite, PersonneLangue, PersonneTravel
from app.views.common import CommonView, LoginRequiredMixin
from app.views.common_mixins import PubliciteMixin, ProgressionMixin


class EditView(LoginRequiredMixin, PubliciteMixin, ProgressionMixin,
               generic.UpdateView):
    model = Personne
    template_name = 'my_home/profile/base.html'
    form_class = ProfileForm
    success_url = reverse_lazy('my_home_profile_edit')

    def get(self, request, *args, **kwargs):
        retour = super(EditView, self).get(request, renderer=None, *args, **kwargs)
        # (!) il ne calcule la vue que si nécessaire !
        # -> forcer à le faire *AVANT* de supprimer le message :
        retour.render()
        if self.request.session.get('message', None):
            del self.request.session['message']
        return retour

    def get_initial(self):
        """
        get_initial() sert à pré-remplir avec des valeurs
        les champs du formulaire via initial['nom_du_champ']
        """
        initial = super(EditView, self).get_initial()

        def apply_initial(idx, obj, prop, l):
            a = getattr(obj, prop)
            initial[idx] = a if a else ''

        u = self.request.user
        apply_initial('user_first_name', u, 'first_name', False)
        apply_initial('user_last_name', u, 'last_name', False)
        apply_initial('email', u, 'email', False)

        p = Personne.objects.get(user=u)
        apply_initial('statut', p, 'statut', False)
        apply_initial('date_naissance', p, 'date_naissance', True)
        apply_initial('field_place_of_birth', p, 'place_of_birth', True)
        apply_initial('field_place_i_live', p, 'place_i_live', True)
        apply_initial('field_employer_current', p, 'employer_current', True)
        apply_initial('field_employer_previous', p, 'employer_previous', True)

        """
        (!!) Suppression des tags dynamiques sur demande de Franck
        """
        def get_tags_with_value(many_to_many_class, type_tag, filtre):
            return [i[0] for i in TagTraduit.objects.filter(
                langue__locale__exact=translation.get_language(),
                tag__type_tag__exact=type_tag,
                pk__in=[i[0] for i in many_to_many_class.objects.filter(
                    personne__user=self.request.user,
                    date_v_fin=None
                ).values_list(filtre)]
            ).values_list('pk')]
        initial['programmes2'] = get_tags_with_value(
            PersonneProgramme, TagBase.TYPE_MATIERE, 'programme__pk')
        initial['activites2'] = get_tags_with_value(
            PersonneActivite, TagBase.TYPE_ACTIVITE, 'activite__pk')
        initial['hobbies2'] = get_tags_with_value(
            PersonneHobby, TagBase.TYPE_HOBBY, 'hobby__pk')
        initial['types_permis2'] = get_tags_with_value(
            PersonneTypepermis, TagBase.TYPE_PERMIS, 'type_permis__pk')
        initial['personnalites2'] = get_tags_with_value(
            PersonnePersonnalite, TagBase.TYPE_PERSONNALITE, 'personnalite__pk')
        initial['langues2'] = get_tags_with_value(
            PersonneLangue, TagBase.TYPE_LANGUE, 'langue__pk')

        return initial

    def get_object(self, queryset=None):
        p = Personne.objects.filter(
            user__pk__exact=self.request.user.pk
        ).all()
        return p[0] if len(p) else None

    def get_context_data(self, **kwargs):
        common = CommonView(self)
        context = super(EditView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('My account')

        if self.object:
            context['url_photo_profil'] = self.object.url_photo_profil
            context['url_photo_banniere'] = self.object.url_photo_banniere
        else:  # Calculer photo sans rien = photo "vide"
            context['url_photo_profil'] = PictureURL().get_url()
            context['url_photo_banniere'] = PictureURL().get_url()

        # (!) Formes supplémentaires :
        context['form_visibilite'] = ProfileVisibiliteForm(
            instance=common.infos['personne'])

        reset_password = self.request.session.get('reset_password')
        if reset_password:
            del self.request.session['reset_password']
        context['form_password'] = ProfilePasswordForm(
            show_field_old_password=not reset_password
        )
        context['form_account_desactivate'] = ProfileDesactivateForm()
        context['form_account_delete'] = ProfileDeleteForm()
        context['form_newsletter_configuration'] = \
            ProfileNewsletterConfigurationForm({
                'newsletter_configuration':
                    common.infos['personne'].newsletter_configuration
            })

        # Comme partout ailleurs, effacer le message s'il y en avait un :
        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']

        # Publicités :
        context['publicites_gauche'] = \
            self.publicites(Publicite.PUBLICITE_MY_PROFILE_GAUCHE)
        context['publicites_droite'] = \
            self.publicites(Publicite.PUBLICITE_MY_PROFILE_DROITE)

        p = Personne.objects.get(user=self.request.user)
        # Progression :
        if self.request.session.get('progression', None) is None:
            self.request.session['progression'] = False
        if not self.request.session['progression']:
            self.request.session['progression'] = True
            context['progression'] = self.progression(self.request.user, p)

        return context

    def form_valid(self, form):

        obj = self.object

        def update_field(post_field, class_field, field_name):
            try:
                values = form.cleaned_data.pop(post_field)
                # Faudrait les marquer comme "périmés" = changer date_v_fin
                # à now(), mais je les supprime. À changer si le site
                # devient tellement énorme qu'on peut tout tracer :
                class_field.objects.filter(personne=obj).delete()
                for pk_str in values:
                    try:
                        v = TagTraduit.objects.get(pk=int(pk_str))
                        p = class_field.objects.create(**{'personne': obj,
                                                          field_name: v})
                        p.save()
                    except (ValueError, LookupError):
                        break  # hack = tout stopper
            except KeyError:
                pass

        update_field('programmes2', PersonneProgramme, 'programme')
        update_field('activites2', PersonneActivite, 'activite')
        update_field('hobbies2', PersonneHobby, 'hobby')
        update_field('types_permis2', PersonneTypepermis, 'type_permis')
        update_field('personnalites2', PersonnePersonnalite, 'personnalite')
        update_field('langues2', PersonneLangue, 'langue')

        # (!!) Note : User = clé étrangère = pas mis à jour automatiquement
        u = User.objects.get(pk=self.request.user.pk)
        u_first_name = form.cleaned_data.get('user_first_name')
        u_last_name = form.cleaned_data.get('user_last_name')
        u_email = form.cleaned_data.get('email')
        if u_first_name or u_last_name or u_email:
            if u_first_name:
                u.first_name = u_first_name
            if u_last_name:
                u.last_name = u_last_name
            if u_email:
                u.email = u_email
            u.save()

        if form.cleaned_data.get('field_picture'):
            # Marquer l'ancienne photo comme n'étant plus valide :
            PersonnePhoto.objects \
                .filter(personne=self.object,
                        photo_type=PersonnePhoto.PHOTO_PROFIL) \
                .update(date_v_fin=make_aware(django_datetime.now()))
            # Créer la nouvelle photo :
            f = form.cleaned_data['field_picture']
            photo = Photo.objects.create(image=f)
            photo.save()
            pp = PersonnePhoto.objects.create(
                personne=self.object, photo=photo,
                photo_type=PersonnePhoto.PHOTO_PROFIL
            )
            pp.save()

        if form.cleaned_data.get('field_picture_banner'):
            # Marquer l'ancienne photo comme n'étant plus valide :
            PersonnePhoto.objects \
                .filter(personne=self.object,
                        photo_type=PersonnePhoto.PHOTO_BANNIERE) \
                .update(date_v_fin=make_aware(django_datetime.now()))
            # Créer la nouvelle photo :
            f = form.cleaned_data['field_picture_banner']
            photo = Photo.objects.create(image=f)
            photo.save()
            pp = PersonnePhoto.objects.create(
                personne=self.object, photo=photo,
                photo_type=PersonnePhoto.PHOTO_BANNIERE
            )
            pp.save()

        # Champs faits automatiquement via déclaration de la forme / Meta
        self.request.session['message'] = (
            _('Congratulations, your profile has been successfully updated!'),
            _('Please note that you can amend all practical and optional '
              'information, and also check out the online help section, '
              'at any time via your profile.'),
            '',
            '<b>{}</b>'.format(
                _('Please also bear in mind that a more complete profile '
                  'will attract more attention. Increase your chances!')
            ),
            _('Close'),
        )
        return super(EditView, self).form_valid(form)
#
