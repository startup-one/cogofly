# coding=UTF-8
# Page statique : "À propos"


from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _

from app.models.personne import ActiviteTestimony
from app.views.common import CommonView


class TestimoniesView(View):
    template_name = 'static/testimonies.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'temoignages': ActiviteTestimony.objects.filter(
                validated_by_moderator=True,
                date_v_fin__exact=None),
            'testimonies_title': _('Cogofly - Testimonies'),
            'testimonies': [{
                'title': _('Olivier Foulon:'),
                'details': _(
                    '"Having had the chance to work together with FRANCK on '
                    'several projects, I have had the opportunity to '
                    'accompany him on several business trips; he is the kind '
                    'of guy you will never forget, always willing to provide '
                    'assistance to all kinds of people. I believe it is part '
                    'of his genetic profile to be on Earth, help people and '
                    'make them happy, in both small and great ways. I believe '
                    'his site is part of this process and constitutes a real '
                    'inner part of his personality; almost as if it were the '
                    'logical conclusion to a personal ambition dedicated to '
                    'fulfilling everybody\'s needs and, more precisely, '
                    'passion for travelling, and the embedded necessity for '
                    'everybody to interchange.'
                )}, {
                'title': _('Michel Wauthier:'),
                'details': _(
                    '"I have known Franck for quite a while now. He has a '
                    'unique way of meeting people, striking up relationships, '
                    'genuine and sincere ones, and is very loyal when it '
                    'comes to friendship. Always on the move, dynamic, full '
                    'of new ideas, with a real entrepreneurial spirit, he has '
                    'shown courage and determination by putting everything he '
                    'has into a project in which he wholeheartedly believes; '
                    'a project with the goal of bringing people closer '
                    'together, and getting them to meet up with each other. A '
                    'project which, upon reflection, resembles him a great '
                    'deal; and it is for this reason that it has to work. And '
                    'not just for him, but for those whom it will help to '
                    '"co-go-fly": new faces for new trips and places.'
                )}, {
                'title': _('Benjamin Mallows:'),
                'details': _(
                    '"I\'ve known Franck for several years now and his will '
                    'to succeed, drive and motivation are simply second '
                    'to none. It\'s a real pleasure to work with people '
                    'like Franck because you always have that peace of mind, '
                    'safe in the knowledge that results are guaranteed. '
                    'Franck is a loyal and trustworthy colleague and '
                    'friend who, I have no doubt about it, has the '
                    'profile and all the prerequisites to be the very best. '
                    'His project is a fascinating one and I\'m very much '
                    'looking forward to seeing all of his hard '
                    'work pay off."'
                )}, {
                'title': _('Florent Portes:'),
                'details': _(
                    '"Franck is the designer and creator of this website, he '
                    'asked me to help him for the development, I was '
                    'motivated by this idea to find a solution for all these '
                    'people that don’t want to travel alone, indeed, times '
                    'are difficult these days, for all, economic crisis, '
                    'current situation, terrorism but the fact you can find '
                    'hope despite all these bad things happening is first of '
                    'all a noble idea and to take a stand in this world, and '
                    'to see few persons motivated to develop this project, '
                    'this is a really creative and innovative idea, to allow '
                    'people that don’t know each other, to meet, travel and '
                    'the more you get to know someone, the closer you feel to '
                    'them, and these friendships will last, because love is '
                    'stronger than all things, and we need to defend this '
                    'love in this chaotic world today. '
                    'Franck is a committed person, I have only known him for '
                    'a few years but what struck me is his strength of '
                    'conviction, close to stubbornness but to do good, and to '
                    'seek quality, what struck me again is his motivation, he '
                    'refuses to fail, I am motivated to work with him to see '
                    'these qualities and concepts in him, his desire to '
                    'succeed and to bring forth his vision, because it is '
                    'with small and simple things that great things are '
                    'achieved."'
                )}]
        })
