# coding=UTF-8


from django.forms import widgets


class GoogleMapsWidget(widgets.Input):
    is_required = False

    def __init__(self, attrs=None):
        if attrs:
            v = attrs.get('class', '')
            attrs['class'] = (v+' gmaps-autocomplete').strip()
        else:
            attrs = {}
        attrs['autocomplete'] = 'off'
        super(GoogleMapsWidget, self).__init__(attrs)
