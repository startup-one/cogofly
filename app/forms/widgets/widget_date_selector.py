# coding=UTF-8


from datetime import datetime
from django import utils
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _

from app.models.date_partial import DatePartial
import six
from six.moves import range
from six.moves import zip


class DateSelectorWidget(widgets.MultiWidget):

    def __init__(self, attrs=None):
        self.errors = []
        self.date_partial = None
        # ajouter les hints ainsi que les attributs HTML5 min et max :
        if attrs is None:
            a = {}
        else:
            a = attrs
        attrs_days = a.copy()
        attrs_days['min'] = 1
        attrs_days['max'] = 31
        attrs_days['placeholder'] = _('DD')
        attrs_months = a.copy()
        attrs_months['min'] = 1
        attrs_months['max'] = 12
        attrs_months['placeholder'] = _('MM')
        attrs_years = a.copy()
        attrs_years['min'] = 1930 if a.get('min') is None else a['min']
        attrs_years['max'] = 2020 if a.get('max') is None else a['max']
        attrs_years['placeholder'] = _('YYYY')

        def custom_list(deb, fin, reverse=False):
            if reverse:
                b = list(range(fin, deb-1, -1))
            else:
                b = list(range(deb, fin+1))
            b = list(zip(b, [six.text_type(c).rjust(2, '0') for c in b]))
            b.insert(0, ('**', '-'))
            return b

        _widgets = (
            widgets.Select(choices=custom_list(1, 12), attrs=attrs_months,),
            widgets.Select(choices=custom_list(1, 31), attrs=attrs_days,),
            widgets.Select(choices=custom_list(attrs_years['min'],
                                               attrs_years['max'], True),
                           attrs=attrs_years,),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        # devrait tout le temps avoir une valeur du type "YYYY-MM-DD"
        # avec éventuellement DD à '**' ou MM à '**'
        # print('decompress')
        # print(value)
        if type(value) in [str, six.text_type]:
            try:
                # Essai d'assigner, si pas bonne date, exception ValueError :
                yy, mm, dd = value.split('-')
                # Test date existante sinon ValueError :
                datetime(year=int(float(yy)) if yy != '**' else 2000,
                         month=int(float(mm)) if mm != '**' else 1,
                         day=int(float(dd)) if dd != '**' else 1)
            except ValueError:
                return [None, None, None]
            return [mm, dd, yy]
        elif value:
            return [value.month, value.day, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        # print(rendered_widgets)
        # En français, inverser mm et jj
        # (!) = par défaut format anglais, mais changer que si français :
        #       -> PAS MULTILANGUE MAIS JE N'AI PAS LE TEMPS :
        l = utils.translation.get_language().split('-')[0]
        r = rendered_widgets
        if l == 'fr':  # inverser mm <=> jj
            k = [r[1], r[0], r[2]]
        else:
            k = r
        return '&nbsp;'.join(k)

    def value_from_datadict(self, data, files, name):
        if self.date_partial:  # déjà précalculé
            return str(self.date_partial)
        self.errors = []
        if type(data) is dict:
            return data[name] if name in data else None
        if type(data) is not QueryDict:
            f = data.getattr(name)
            if type(f) is datetime or (not f):
                # Vient de la base de données ou None = pas toucher
                return data[name]

        # Arrivé ici = post qui vient du Web -> aller récupérer les valeurs :
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        # print(datelist)
        # print('Valeur extraite du post :', str(datelist))
        try:
            mm = int(datelist[0]) if datelist[0] != '**' else None
            dd = int(datelist[1]) if datelist[1] != '**' else None
            # print('dd', dd)
            # print('mm', mm)
            # print('ok, tentative...')
            self.date_partial = DatePartial(dd=dd, mm=mm, year=int(datelist[2]))
        except TypeError:
            return None
        except ValueError:
            return None
        except AssertionError as e:
            self.errors.append(e.message)
            return None
        else:
            return str(self.date_partial)
