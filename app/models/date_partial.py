# coding=UTF-8


import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class DatePartial(object):

    def __init__(self, year, mm=None, dd=None):
        if not year:
            raise AssertionError(_("Year can't be None"))
        if dd and (not mm):
            raise AssertionError(_("Day must be None if month is None"))
        self.ignore_mm = (mm is None)
        self.ignore_dd = (dd is None)
        if self.ignore_mm:
            self.date = datetime.date(int(year), 1, 1)
        elif self.ignore_dd:
            self.date = datetime.date(int(year), int(mm), 1)
        else:
            self.date = datetime.date(int(year), int(mm), int(dd))

    def __lt__(self, other):
        if isinstance(other, datetime.datetime):
            if self.year < other.year:
                return True
            if self.year > other.year:
                return False
            # Arrivé ici -> années égales, tester le mois
            if self.ignore_mm:
                return False
            if self.month < other.month:
                return True
            if self.month > other.month:
                return True
            # Arrivé ici -> mois égaux, tester le jour
            return self.day < other.day
        # sinon, on essaie de comparer les chaines :
        return str(self) < str(other)

    def __str__(self):
        return '{:0>4}-{:0>2}-{:0>2}'.format(
            self.date.year,
            self.date.month if not self.ignore_mm else '**',
            self.date.day if not self.ignore_dd else '**')

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month if not self.ignore_mm else '**'

    @property
    def day(self):
        return self.date.day if not self.ignore_dd else '**'

    @property
    def canonical_version(self):
        if self.ignore_mm:
            return date_format(self.date, 'Y')
        if self.ignore_dd:
            return date_format(self.date, 'E Y')
        return date_format(self.date, 'DATE_FORMAT')

