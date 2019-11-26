# coding=UTF-8


from django.core.exceptions import ValidationError
from django.db import models

from app.forms.generic.fields.field_date_partial import FormFieldDatePartial
from app.models.date_partial import DatePartial


def parse_date_partial(value):
    if (value == 'None') or (value is None) or (not value):
        return None
    # print('parse_date_partial')
    # print('value', str(value), type(value))

    a = value.split('-')
    if len(a) != 3:
        raise ValidationError('Invalid DatePartial value')
    try:
        return DatePartial(
                int(a[0]),
                int(a[1]) if a[1] not in ['0*', '**'] else None,
                int(a[2]) if a[2] not in ['0*', '**'] else None)
    except ValueError:
        raise ValidationError('Invalid DatePartial value')


class DatePartialField(models.Field):

    description = "Date that may be partial (without day or even without month)"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # "YYYY-MM-DD"
        super(DatePartialField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DatePartialField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    def from_db_value(self, value, expression, connection, context):
        return parse_date_partial(value)

    def to_python(self, value):
        if isinstance(value, DatePartialField):
            return value

        return parse_date_partial(value)

    def get_prep_value(self, value):
        # value = DatePartial, la convertir simplement en chaîne :
        if (value == 'None') or not value:
            return None
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(self.get_prep_value(value))

    def formfield(self, **kwargs):
        defaults = {'form_class': FormFieldDatePartial}
        defaults.update(kwargs)
        return super(DatePartialField, self).formfield(**defaults)

# @python_2_unicode_compatible
# class DatePrecision(models.Model):
#     PRECISION_CHOICES = (
#         (0, 'precise'),
#         (1, 'month'),
#         (2, 'year'),
#         (3, 'decade'),
#         (4, 'century'),
#     )
#     """
#     Récupéré ici, puis modifié pour mes besoins :
#     https://github.com/
#     malcolmt/django-modeling-examples/blob/master/dates/models.py
#     Dates with precision measurements. This class is a little naïve when it
#     comes to really ancient dates: it doesn't take calendar changes into
#     consideration. Every year has 365 days, for example (if you think that's
#     a given, look at September, 1752 when you have a spare moment).
#     """
#     date = models.DateField()
#     precision = models.IntegerField(default=0, choices=PRECISION_CHOICES)
#
#     def __str__(self):
#         # XXX: Work around fact that strftime() cannot usually handle years
#         # prior to 1900.
#         tmp_date = self.date.replace(year=1900)
#         date_str = u"%s, %s" % (tmp_date.strftime("%d %b"), self.date.year)
#         if self.precision == 0:
#             return date_str
#         return u"%s containing %s" % (self.get_precision_display(), date_str)
#
#     def to_string(self):
#         return u'{:0>4}-{:0>2}-{:0>2}-{:0>2}'.format(
#             self.date.year, self.date.month, self.date.day, self.precision)
#
#     def from_string(self, s):
#         a = s.split(u'-')
#         if len(a) < 4:
#             raise AssertionError(_(u'Invalid DatePrecision format'))
#         self.precision = int(a[3])
#         if self.precision == 0:
#             return self.date
#         if self.precision == 1:
#             return datetime.date(1, self.date.month, self.date.year)
#         if self.precision == 2:
#             return datetime.date(1, 1, self.date.year)
#         if self.precision == 3:
#             new_year = 1 + 10 * ((self.date.year - 1) / 10)
#             return datetime.date(1, 1, new_year)
#         if self.precision == 4:
#             new_year = 1 + 100 * ((self.date.year - 1) / 100)
#             return datetime.date(1, 1, new_year)
#         raise AssertionError(_(u'Unknown precision'))
#
#     def canonical_version(self):
#         """
#         Renvoie une version canonique de la date. Pour les tris et comparaisons.
#         C'est la date au plus tôt de l'intervalle.
#         Par exemple, 1/1/1903 et 6/6/1901 avec précision 'decade' ont toutes
#         les deux une version canonique de 1/1/1901 (AVEC PRÉCISION 'decade').
#         Centuries et decades sont tous les deux traités sur l'année qui termine
#         par 1 (ex. 1901, plutôt que 1900).
#         """
#         precision = self.precision
#         if precision == 0:
#             return self.date
#         if precision == 1:
#             return datetime.date(1, self.date.month, self.date.year)
#         if precision == 2:
#             return datetime.date(1, 1, self.date.year)
#         if precision == 3:
#             new_year = 1 + 10 * ((self.date.year - 1) / 10)
#             return datetime.date(1, 1, new_year)
#         if precision == 4:
#             new_year = 1 + 100 * ((self.date.year - 1) / 100)
#             return datetime.date(1, 1, new_year)
#         raise AssertionError(_(u'On ne devrait jamais arriver ici'))
