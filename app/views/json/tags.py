# coding=UTF-8


from django.http import JsonResponse
from django.utils import translation
from django.views import generic

from app.models.tag import TagWithValue
from app.views.common import LoginRequiredMixin


class JsonTagsView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return JsonResponse({'items': ['hackers welcome!'], 'total': 1})


class JsonTagsWithValueView(JsonTagsView):
    type_tag = None

    def get(self, req, *args, **kwargs):
        r = req.GET.get('q', '')
        a = list(TagWithValue.objects
                 .filter(langue__locale__exact=translation.get_language(),
                         type_tag__exact=self.type_tag,
                         value__contains=r)
                 .values('pk', 'value'))
        a = [{'id': b['pk'], 'item':b['value']} for b in a]
        return JsonResponse({'items': a, 'total': len(a)})


class JsonTagsLangagesView(JsonTagsWithValueView):
    type_tag = TagWithValue.TYPE_LANGUE


class JsonTagsTypesPermisView(JsonTagsWithValueView):
    type_tag = TagWithValue.TYPE_PERMIS


class JsonTagsDiplomesView(JsonTagsWithValueView):
    type_tag = TagWithValue.TYPE_PERMIS


class JsonTagsCentresDInteretView(JsonTagsWithValueView):
    type_tag = TagWithValue.TYPE_PERMIS


class JsonTagsHobbiesView(JsonTagsWithValueView):
    type_tag = TagWithValue.TYPE_HOBBY


