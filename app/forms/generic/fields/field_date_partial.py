# coding=UTF-8


from django import forms
from app.forms.widgets.widget_date_selector import DateSelectorWidget


class FormFieldDatePartial(forms.Field):
    widget = DateSelectorWidget


