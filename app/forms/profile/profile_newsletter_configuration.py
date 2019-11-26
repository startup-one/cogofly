# coding=UTF-8


from django import forms
from django.utils.translation import ugettext_lazy as _

from app.forms.generic.generic import FormForceLocalizedDateFields
from app.models.personne import Personne
from app.models.personne_enums import PersonneEnums


class ProfileNewsletterConfigurationForm(FormForceLocalizedDateFields):

    class Meta:
        model = Personne
        fields = ('newsletter_configuration',)

    e = {'required': _('This field is required'),
         'invalid': _('This field contains invalid data')}

    a = _('When do you want to receive your dashboard '
          'and other notifications?')
    newsletter_configuration = forms.IntegerField(
        # help_text=_(u'Change your newsletter configuration here:'),
        label=a,
        widget=forms.Select(attrs={
            # 'helpcolor': '#f85a29',  # champ custom
            'title': a,
            'groupno': 0,
            'class': 'form-control',
            'rowstart': True,
            'rowspan': 12,
            'rowend': True, },
            choices=[(k, PersonneEnums.TAB_NEWSLETTER_CONFIGURATION[k])
                     for k in PersonneEnums.TAB_NEWSLETTER_CONFIGURATION]),
        error_messages=e)

