# coding=UTF-8


from django.forms import widgets
from django.utils.translation import ugettext_lazy as _


class Select2Widget(widgets.SelectMultiple):
    """
    Classe pour crée un widget qui doit se remplir en faisant des appels JSON
    (!) Pour que cela fonctionne, il faut passer l'URL en tant qu'attribut
        via 'data-select2-json',
    Exemple :
            known_languages = forms.CharField(
                label=a, max_length=100,
                widget=Select2Widget(attrs={
                    'title': a,
                    'placeholder': _(u'type here your known languages'),
                    'data-select2-json': reverse_lazy('json_url_langues'),
                    'class': 'form-control'}),
                error_messages=self.e)
    """
    def __init__(self, attrs=None):
        attrs = attrs if attrs else {}
        if not attrs.get('data-select2-json'):
            raise Exception(_('data-select2-json class needed'))
        super(Select2Widget, self).__init__(attrs)

    def validate(self, value):
        retour = super(Select2Widget, self).validate(value)
        return retour
