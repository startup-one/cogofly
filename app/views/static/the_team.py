# coding=UTF-8
# Page statique : "À propos"


from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _


class TheTeamView(View):
    template_name = 'static/the_team.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'the_team_title': _('Cogofly - The team'),
            'the_team_who_are_we': _('Who are we?'),
            'the_team_stories': [_(
                '<strong>COGOFLY</strong> was founded by Mr. Franck '
                'Lagathu, born on 21 June 1973 in Marseille, France.'
            ), _(
                'Commercial Support Manager at Airbus Helicopters, and '
                'former Sales Manager in the Estate Agents sector, the '
                'launch of this new site marks the start, in parallel, of '
                'a new and passionate adventure. Whilst I have a great '
                'team supporting me, as the main player it is important '
                'to talk about my own diverse experiences in order to '
                'explain how the idea of launching such a concept came '
                'about.'
            ), _(
                'The first page written, or rather "scribbled", during '
                'the summer of 2006 highlighted the need for a concept '
                'which would later become part of the '
                '<strong>COGOFLY</strong> adventure. It was indeed the '
                'result of a simple observation: <strong>There are far '
                'too many people who travel alone!</strong>'
            ), _(
                'At the time, with this worldwide phenomenon in mind, my '
                'site was leaning towards a name that I would later deem '
                'to be overly "pessimistic": <strong>Never Alone!</strong>'
            ), _(
                'The fact that I was based in Munich for 4 years, along '
                'with other commitments, meant that I had to put the '
                'project on the backburner for a while. However I NEVER '
                'forgot about it...in fact quite the contrary! I was '
                'constantly writing down different ideas and closely '
                'following the global market. It was clear to me that the '
                'entire world was concerned and I felt I had to do '
                'something to address this universal issue.'
            ), _(
                'Always there for my family and friends, this desire to '
                'always help people out encouraged me to launch a website '
                'which could respond to this requirement in every way. '
                'The testimonies that can be found on this site only '
                'serve to reinforce this temperament which is fully '
                'recognized and appreciated by my entourage; a '
                'temperament which, quite naturally, resulted in a '
                'connection between this site and my destiny.'
            ), _(
                'Back from Germany in 2010, after a multitude of fruitful '
                'and enriching encounters, I was able to restart work on '
                'my ideas which had by now reached a dozen pages. The 5 '
                'years following my return home only served to strengthen '
                'the courage of my convictions, and several useful pages '
                'were added in order to further the project and work '
                'towards something more concrete.'
            ), _(
                '2015 has been a crucial year in that I have had the '
                'chance to meet a number of people within the sector, '
                'along with web service providers, and have thus learned '
                'a great deal from being in their presence. These '
                'contacts, located via a list given to me by Marseille’s '
                'Chamber of Commerce and Industry (CCI), through their '
                'respective remarks and feedback regarding my concept, '
                'have only served to strengthen my desire to proceed with '
                'the launch of this new social network on an '
                'international scale.'
            ), _(
                'The support of this institution helped me to realize '
                'that a number of additional skills were required, such '
                'as legal, financial and HR-related aspects...as is the '
                'case for any newfound company. Thanks to them, I was '
                'able to obtain all of the contacts required in order to '
                'set me on the right path...'
            ), _(
                'All of these encounters resulted in me finding another '
                'name, more internationally orientated, which expressed '
                'the idea of taking off...<strong>Take Off Mate '
                '(TOM)</strong> was therefore brought to the table. At '
                'this point I have to say a big thank you to several of '
                'my work colleagues who took the time to motivate me and '
                'give me their opinions in order to ratify each key step '
                'of my project.'
            ), _(
                'It was with this name that I was able to present it to '
                'the Masters students at the University of Aix-Marseille '
                'at Luminy, more precisely to the <strong>Junior '
                'Aix-Marseille company (JAM), presided by Mr Florian '
                'DOUAY</strong> who, with the support of two other '
                'contributors, came up with a 43-page technical '
                'specification. It was therefore only normal to choose '
                'this establishment, and the choice was made even more '
                'quickly due to the fact that the students’ were '
                'instantly motivated, willing and full of ideas; fully in '
                'line with the ethics of this site.'
            ), _(
                'As I turned the pages of the technical specification, it '
                'seemed to suit me more and more, and I felt the need to '
                'make the adequate changes in order to add the finishing '
                'touches. The changes carried out helped to form the '
                'foundations of this site.'
            ), _(
                'Once the new 50-page version approved, my attention then '
                'turned towards <strong>HQF Development, and its '
                'representative Sir Olivier PONS</strong>, who convinced '
                'me to finally take the plunge with this '
                'international-scale project. His reactivity, honest '
                'approach throughout our different exchanges, passion and '
                'a general feel-good factor that I got from him, led '
                'quite naturally to <strong>the signing of a development '
                'contract on 5 October 2015.</strong>'
            ), _(
                'As indicated in the "About COGOFLY" section, '
                '<strong>COGOFLY</strong> was therefore created one week '
                'before the signing of the said contract, and the brand '
                'was then deployed on a global scale.'
            ), _(
                '<strong>My goal is to make this new social network the '
                'reference in terms of co-trips: "The LinkedIn/Facebook" '
                'of the Tourism industry. This new community will then '
                'have access to a reliable and intuitive site, and be '
                'able to meet up in total confidence and share common '
                'projects and goals.</strong>'
            ), _(
                'The conclusion of all this, and this adage came to me '
                'quite naturally, is that:'
            ), _(
                '<h1>Alone, we think...Together, we get away!</h1>'
            )]
        })
