# coding=UTF-8
# Page statique : "À propos"


from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _


class AboutView(View):
    template_name = 'static/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'about_title': _('About Cogofly'),
            'about_main_aim': _(
                'The main aim of this page is to explain the Cogofly concept.'
                'The brand Cogofly, name and logo, came to light thanks to '
                'the human values that this concept wishes to get across and '
                'maintain moving forward.'),
            'about_constat': _(
                'This brand is the result of a worldwide issue: '
                '<strong>There are far too many people who travel '
                'alone!</strong>'),
            'about_concept_title': _('The concept:'),
            'about_concept_content_1': _(
                'The idea came to light after several professional and '
                'private trips I have been able to do over the years...'),
            'about_concept_content_2': _(
                '<strong>This social network website is a worldwide concept'
                ' which will help to avoid travelling, spending a weekend, '
                'make a business trip, do some rides (cultural, sport, '
                'education, etc...), or just going on an outing, ALONE...'
                'if someone just feel ALONE, as well and for any reasons, '
                'this website is then the good one !</strong>'),
            'about_concept_content_3': _(
                'This situation, unfortunately, doesn\'t have "borders"...'
                'It can touch a person, a group of person, couples, families '
                'and also all socio-professional categories. '),
            'about_concept_content_4': _(
                '<strong>Cogofly\'s primary goal is to help people to avoid '
                'travelling alone any more. The second one is simply to help '
                'them to no longer be alone.</strong>'),
            'about_concept_content_5': _(
                'It also naturally deals with the following notion:<strong>: "'
                'Who has never felt like they\'re always well surrounded, '
                'but ended up feeling rather alone ?</strong>'),
            'about_brand_title': _('The brand: name + logo'),
            'about_brand_content_1': _(
                'It was of paramount importance to find a site name which '
                'was both catchy and easy to remember for all members, plus '
                'anyone else reading this page (verbally and visually).'),
            'about_brand_content_2': _(
                '<strong>It was therefore absolutely necessary to '
                'find:</strong>'),
            'about_brand_content_li_1': _(
                'A short name, easy to pronounce and remember (Facebook, '
                'Google, Twitter, Airbnb, Viadeo, etc...).'),
            'about_brand_content_li_2': _(
                'A simple, clear and visual logo.'),

            'about_name_title': _('Name:'),
            'about_name_content_1': _(
                'In order for this mission to succeed, it was important to '
                'keep certain ideas and "basic" words in mind, such as:'),
            'about_name_content_2': _(
                'Sharing: co-travelling, car-sharing...'),
            'about_name_content_3': _(
                'Going out / Being on the move: trips, excursions, '
                'days/nights out...'),
            'about_name_content_4': _(
                'Travelling: going away, heading off, jetting off...'),
            'about_name_content_5': _(
                '<strong>CO-GO-FLY</strong>: The name seemed so '
                '<strong>OBVIOUS</strong>!'),
            'about_name_content_6': _(
                '<strong>And so Cogofly was born, its domain name reserved '
                'on Monday 28 September 2015 and its trademark protected '
                'with INPI</strong>!'),


            'about_logo_title': _('Logo:'),
            'about_logo_content_1': _(
                '<strong>In order to complete this mission, it was important '
                'to highlight:</strong>'),
            'about_logo_content_li_1': _(
                'The "Co" concept, which encapsulates the site\'s main '
                'focus: Think "together", Think "Co" and Take Off!'),
            'about_logo_content_li_2': _(
                'The infinity sign, ∞, which resembles Co...evoking the '
                'infinite possibilities that the site will bring with its '
                'official launch on 21/06/2016.'),
            'about_logo_content_li_3': _(
                'The "smile" situated under the name, more precisely under '
                'the "Gofly" part, and forming a loop around "Co".'),
            'about_logo_content_li_4': _(
                'A "smile" which also evokes the idea of an open and '
                'accessible world.'),
            'about_logo_content_li_5': _(
                'The separation between the 2 semi-circles is intentional, '
                'calling to mind the concept of Yin & Yang, and further '
                'eliciting the need to travel together...'),
            'about_logo_content_li_6': _(
                'A slightly tilted circle in order to express the idea '
                'of movement'),
        })
