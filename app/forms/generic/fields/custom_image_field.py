# coding=UTF-8


from django import forms


class CustomImageField(forms.ImageField):

    def __init__(self, *args, **kwargs):
        self.picture_attributes = kwargs.pop("picture_attributes", None)
        super(CustomImageField, self).__init__(*args, **kwargs)
