# coding=UTF-8

import datetime
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views import generic

from app.forms.personne_travel import PersonneTravelForm
from app.models.date_partial_field import parse_date_partial
from app.models.publicite import Publicite
from app.models.tag import TagWithValue, TagGoogleMapsTraduit
from app.models.personne import Personne, PersonneTravel
from app.views.common import LoginRequiredMixin, CommonView
from app.views.common_mixins import PubliciteMixin


class IndexView(LoginRequiredMixin, PubliciteMixin, generic.FormView):
    template_name = 'my_home/travels/base.html'
    form_class = PersonneTravelForm
    success_url = reverse_lazy('my_home_travel')

    def get_context_data(self, **kwargs):
        # Méga hack : si jamais il y a une erreur sur la forme,
        # et que cette erreur fait partie d'une forme qu'on a édité = avec 'pk'
        # alors la mettre de côté dans form_erreur et à la place, mettre
        # une forme vide pour faire croire que tout va bien :
        form = kwargs.get('form')
        form_erreur_pk = None
        if hasattr(form, 'cleaned_data') and form.cleaned_data.get('pk'):
            if not form.is_valid():  # hasattr(form, 'errors')
                # Mettre de côté cette forme qu'on utilisera plus tard :
                v = form.cleaned_data.get('travel')
                v = v.formatted_address \
                    if type(v) is TagGoogleMapsTraduit else str(v)
                form_erreur_pk = form.cleaned_data['pk']
                form_erreur = PersonneTravelForm(data={
                    'pk': form_erreur_pk,
                    'travel': v,
                    'date_start': form.cleaned_data.get('date_start'),
                    'date_end': form.cleaned_data.get('date_end'),
                    'comments': form.cleaned_data.get('comments'),
                    'field_photo_1': form.cleaned_data.get('field_photo_1'),
                    'field_photo_2': form.cleaned_data.get('field_photo_2'),
                    'field_photo_3': form.cleaned_data.get('field_photo_3'),
                })
                form_erreur.add_error(None, form.errors)
                # Créer la forme "officielle" = insert = vide
                kwargs['form'] = PersonneTravelForm({})
        common = CommonView(self)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['common'] = common.infos
        context['titre'] = _('My travels')

        # -------------------------
        # Deux sections identiques : 'voyages_passes' et 'voyages_a_venir' :
        def remplir_context(index, tab):
            context[index] = []
            for ptf in tab:
                if form_erreur_pk and ptf.pk == form_erreur_pk:
                    context[index].append({
                        'obj': ptf,
                        'form': form_erreur
                    })
                else:
                    context[index].append({
                        'obj': ptf,
                        'form': PersonneTravelForm(initial={
                            'pk': ptf.pk,
                            'travel': ptf.travel.formatted_address,
                            'date_start': ptf.date_start,
                            'date_end': ptf.date_end,
                            'comments': ptf.comments,
                            'field_photo_1': ptf.photo1,
                            'field_photo_2': ptf.photo2,
                            'field_photo_3': ptf.photo3,
                        })
                    })

        p = Personne.objects.get(user=self.request.user)
        remplir_context('voyages_passes', p.travels_past)

        # Même boucle que la précédente 'voyages_passes'
        remplir_context('voyages_a_venir', p.travels_futur)

        if self.request.session.get('message', None):
            context['message'] = self.request.session['message']
            del self.request.session['message']

        # Publicités :
        context['publicites_gauche'] = \
            self.publicites(Publicite.PUBLICITE_VOYAGES_GAUCHE)
        context['publicites_droite'] = \
            self.publicites(Publicite.PUBLICITE_VOYAGES_DROITE)
        return context

    def form_valid(self, form):
        # Tout récupérer dans des variables locales pour plus de concision :
        fc = form.cleaned_data
        pk = fc.get('pk')
        travel = fc.get('travel')
        # décoder ce qui arrive :
        d_start = parse_date_partial(fc['date_start'])
        d_end = parse_date_partial(fc['date_end'])
        is_past = fc.get('is_past') is True
        comments = fc.get('comments')

        # Dès le début, s'il y a des dates, s'assurer qu'elles sont cohérentes :
        if d_end and d_start:
            if d_end.date > datetime.datetime.now().date() > d_start.date:
                form.add_error('date_start', _("Can't start in the past..."))
                form.add_error('date_end', _("...and end in the future!"))
                # add_error supprime les champs de cleaned_data, les remettre :
                form.cleaned_data.update({'date_start': d_start,
                                          'date_end': d_end})
                return super(IndexView, self).form_invalid(form)

            if d_end.date < d_start.date:
                form.add_error('date_start', _('Start is after date end...'))
                form.add_error('date_end', _('...End is before date starts'))
                # add_error supprime les champs de cleaned_data, les remettre :
                form.cleaned_data.update({'date_start': d_start,
                                          'date_end': d_end})
                return super(IndexView, self).form_invalid(form)

        if pk and not (travel or comments or d_start or d_end):
            # Si le pk est passé ET TOUS les champs sont vides = delete
            try:
                pt = PersonneTravel.objects.get(
                    personne=Personne.objects.get(user=self.request.user),
                    pk=pk,
                )
                pt.date_v_fin = datetime.datetime.now()
                pt.save()
                message = _('Your travel has been removed')
            except PersonneTravel.DoesNotExist:  # Hack devrait jamais arriver
                return super(IndexView, self).form_invalid(form)
        elif not travel:
            form.add_error('travel', _("Travel is mandatory"))
            return super(IndexView, self).form_invalid(form)
        elif pk:  # Mise à jour :
            try:
                pt = PersonneTravel.objects.get(
                    personne=Personne.objects.get(user=self.request.user),
                    pk=pk,
                )
                pt.travel = travel
                pt.date_start = d_start
                pt.date_end = d_end
                pt.is_past = is_past
                pt.comments = comments

                if fc.get('field_photo_1'):
                    pt.photo1 = fc.get('field_photo_1')
                if fc.get('field_photo_2'):
                    pt.photo2 = fc.get('field_photo_2')
                if fc.get('field_photo_3'):
                    pt.photo3 = fc.get('field_photo_3')

                pt.save()
                message = _('Your travel has been updated!')
            except PersonneTravel.DoesNotExist:  # Hack devrait jamais arriver
                return super(IndexView, self).form_invalid(form)
        else:
            PersonneTravel.objects.create(
                personne=Personne.objects.get(user=self.request.user),
                travel=travel,
                date_start=d_start,
                date_end=d_end,
                is_past=is_past,
                comments=comments or None,
                photo1=fc.get('field_photo_1'),
                photo2=fc.get('field_photo_2'),
                photo3=fc.get('field_photo_3')
            )
            message = _('Your travel has been added!')
        self.request.session['message'] = [
            _('Operation successful!'), message,
            _('Click here to hide this message')]

        # (!) j'ai ajouté un paramètre pour passer l'utilisateur :
        return super(IndexView, self).form_valid(form)
