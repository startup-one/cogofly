# coding=UTF-8


from django.db import models
from django.db.models import Count
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from app.models.generic import BaseModel
from app.models.personne import Personne


@python_2_unicode_compatible
class Message(BaseModel):
    src = models.ForeignKey('Personne', on_delete=models.CASCADE,  related_name='message_src')
    dst = models.ForeignKey('Personne', on_delete=models.CASCADE,  related_name='message_dst')
    is_read = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True,
                               verbose_name=_('Messages'))
    # prévenir la destination si elle a un message non lu :
    dst_message_unread_notified = models.DateTimeField(
        default=None, editable=True, null=True,
        verbose_name=_("Destination is notified by mail"))

    src_visible = models.BooleanField(default=True, blank=True,
                                      verbose_name=_('Visible by src'))
    dst_visible = models.BooleanField(default=True, blank=True,
                                      verbose_name=_('Visible by dst'))

    def message_summary(self):
        a = self.message
        if a:
            return (a[:85] + '&raquo;...') if len(a) > 90 else a
        return ''

    def message_to_html(self):
        return self.message.replace('\n', '<br />')

    def __str__(self):
        return '{} : {} <> {} ({}) : "{}"'.format(
            self.date_creation.strftime('%Y-%m-%d %H:%M:%S'),
            self.src.full_name(), self.dst.full_name(),
            _('read') if self.is_read else _('unread'),
            self.message_summary()
        ).strip()

    class Meta:
        ordering = ["date_creation"]


@python_2_unicode_compatible
class Conversation(BaseModel):
    personnes = models.ManyToManyField(Personne,
                                       symmetrical=False,
                                       related_name='conversations')
    messages = models.ManyToManyField(Message,
                                      symmetrical=False,
                                      related_name='conversations')

    def messages_by_date(self):
        return self.messages.all().order_by('-date_last_modif')

    def first_person_who_is_not(self, p):
        return self.personnes.exclude(pk=p.pk)[0]

    def messages_unread_written_by(self, p):
        return self.messages.exclude(is_read=True).filter(src=p)

    def messages_unread_for(self, p):
        return self.messages.exclude(is_read=True).filter(dst=p)

    @staticmethod
    def between(src, dst):
        convs_src = Conversation.objects\
            .annotate(c=Count('personnes'))\
            .filter(c=2, personnes__in=[src.pk]).values_list('pk', flat=True)
        convs_dst = Conversation.objects\
            .annotate(c=Count('personnes'))\
            .filter(c=2, personnes__in=[dst.pk]).values_list('pk', flat=True)
        # code pour faire l'intersection des ids conversations en commun :
        return list(set(list(convs_src)).intersection(list(convs_dst)))

    @staticmethod
    def add_message(src, dst, msg_to_send):
        convs = Conversation.between(src, dst)
        if len(convs):  # get() = pour avoir un objet (!= QuerySet)
            c = Conversation.objects.get(pk=convs[0])
        else:
            c = Conversation.objects.create()
            c.save()
            c.personnes.add(src)
            c.personnes.add(dst)
            c.save()
        m = Message.objects.create(src=src, dst=dst, message=msg_to_send)
        m.save()
        c.messages.add(m)
        c.save()

    def __str__(self):
        return _('Conversation n.{}').format(self.pk).strip()


