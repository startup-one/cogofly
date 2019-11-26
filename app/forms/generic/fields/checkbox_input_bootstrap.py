# coding=UTF-8


from django.forms import CheckboxInput
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class CheckboxInputBootstrap(CheckboxInput):

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        label = final_attrs.pop('label', '')
        if not label and final_attrs['title']:
            label = final_attrs['title']

        a = format_html('<div class="checkbox">'
                        '<label><input{} />{}</label>'
                        '</div>',
                        flatatt(final_attrs), label)
        return a
