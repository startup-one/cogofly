# coding=UTF-8



import random
import time
import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error
from copy import deepcopy
from datetime import timedelta

import re

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse
from django.db.models import Q
from django.utils import translation
from django.utils.formats import get_format
from django.utils.timezone import make_aware
from django.utils.translation import ugettext_lazy as _, ungettext
from django.utils.datetime_safe import datetime as django_datetime
from django_markdown.templatetags.django_markdown import markdown_safe

from app.models.blog import Blog, BlogTraduit
from app.models.personne import Personne, PersonneActiviteNewsletter, \
    PersonneTravel, PersonneSearch, PersonneBlogNewsletter
from app.models.personne_enums import PersonneEnums
from app.models.tag import TagGoogleMapsTraduit, TagGoogleMaps
from app.views.common_mixins import ActivitesMixin, MessagesNotReadMixin, \
    InvitationsMixin, LikesMixin


class Command(ActivitesMixin, MessagesNotReadMixin, InvitationsMixin,
              LikesMixin, BaseCommand):
    help = 'Send the newsletter to members'
    can_import_settings = True

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.requires_system_checks = True  # test bd bien synchro, entre autres
        self.output_transaction = True  # dump visuel de SQL

    def add_arguments(self, parser):
        parser.add_argument('--reset_all_news',
                            action='store_true',
                            dest='reset_all_news',
                            default=None,
                            help='Reset ALL news and resend ALL to EVERYBODY')
        parser.add_argument('--reset_personne_id',
                            action='store_true',
                            dest='reset_personne_id',
                            default=None,
                            help='Reset newsletter of a specific person')
        parser.add_argument('--fake',
                            action='store_true',
                            dest='fake',
                            default=None,
                            help='Just fake and send to Cogofly')

    def send_newsletter(self, personne, nb_mails_sent, fake):

        if personne.site_language is None:
            return
        if personne.site_web is None:
            return

        translation.activate(personne.site_language.locale)
        f = get_format('DATE_INPUT_FORMATS')[1]

        message = []
        html_message = []

        def append_m(msg, html_msg=None, with_newline=True, position=None):
            if position is not None:
                message.insert(position, msg)
                if with_newline:
                    message.insert(position + 1, "\n")
                html_message.insert(position,
                                    msg if html_msg is None else html_msg)
                if with_newline:
                    html_message.insert(position + 1, "\n")
            else:
                if msg != '':
                    message.append(msg)
                if with_newline:
                    message.append("\n")
                html_message.append(msg if html_msg is None else html_msg)
                if with_newline:
                    html_message.append("\n")

        # prendre tous les blogs à envoyer dans la langue de la personne :
        d = make_aware(django_datetime.now())
        # all blogs to send:
        blogs_all = Blog.objects.filter(
            # ! to test :
            # Q(date_envoi_newsletter__isnull=True) |
            Q(date_envoi_newsletter__isnull=False) &
            Q(date_envoi_newsletter__lte=d))
        blogs_traduits_to_send = BlogTraduit.objects.filter(
            blog__in=blogs_all,
            locale__exact=personne.site_language.locale)
        blogs_already_sent = PersonneBlogNewsletter.objects.filter(
            personne=personne).values_list('pk')
        blogs_to_send = blogs_traduits_to_send.exclude(pk__in=blogs_already_sent)
        for b in blogs_to_send:
            content = markdown_safe(b.content).replace(
                '<img ', '<img style="max-width: 100%;" ').replace(
                '[HTML_REMOVED]', '')
            append_m('',
                     '<h1>{}</h1>{}'.format(b.title, content),
                     with_newline=False)

        # prendre toutes les activites dans la langue de la personne :
        news_sent = PersonneActiviteNewsletter.objects.filter(personne=personne)
        activites = self.activites(personne, personne.site_language).exclude(
            pk__in=news_sent.values_list('activite__pk'))

        for activite in activites:
            append_m(
                _("- {}, {}:\n{}\n\n").format(
                    activite.date_last_modif.strftime(f),
                    activite.date_last_modif.strftime('%H:%M'),
                    activite.description(with_date=False)),
                _("- {}, {}:\n{}\n\n").format(
                    activite.date_last_modif.strftime(f),
                    activite.date_last_modif.strftime('%H:%M'),
                    activite.description(
                        with_date=False, tag='b', with_link=True,
                        website=personne.site_web)))

        n = self.messages_not_read(personne).count()
        if n > 0:
            m = ungettext('You have {} message not read.',
                          'You have {} messages not read.', n).format(n)
            append_m(m)
        n = self.messages_not_read(personne).count()
        if n > 0:
            m = ungettext('You have {} invitation not read.',
                          'You have {} invitations not read.', n).format(n)
            append_m(m)
        n = self.likes(personne).count()
        if n > 0:
            m = ungettext('You have {} like!',
                          'You have {} likes!', n).format(n)
            append_m(m)

        # only add if something to say:
        if len(message):
            # !only add before anything else (position=0)
            append_m(str(_("Here is the latest news on your contacts, "
                           "along with other notifications that might be of "
                           "interest to you, since your last connection:")),
                     position=0)

        # # ------------------
        # # remember that without travels you wont be seen in search results:
        # if PersonneTravel.objects.filter(personne=personne).count() == 0:
        #     a = str(_(
        #         u'Important: it is of paramount importance to add a trip, '
        #         u'a weekend or a day out if you want to appear '
        #         u'in the search results '
        #         u'and give yourself the opportunity to meet new cogoflyers!'))
        #     append_m(u'\n')
        #     append_m(
        #         a,
        #         html_msg=u'<b><span style="color:red; ">{}'
        #                  u'</span></b>'.format(a),
        #         with_newline=False, position=0)
        #     append_m(
        #         str(_(u'If you would like to add a travel, '
        #               u'please log in via the following link:')),
        #         with_newline=False, position=1)
        #     append_m(
        #         u"{}{}".format(personne.site_web, reverse('my_home_travel')),
        #         position=2)

        # ------------------
        # add news about new people registered: how many and some travels:
        if personne.newsletter_date_sent is not None:
            first_time = False
            new_people_registered = [p.id for p in Personne.objects.filter(
                date_creation__gt=personne.newsletter_date_sent).
                order_by('-date_creation')]
        else:  # first time newsletter = all people registered
            first_time = True
            new_people_registered = [
                p.id for p in Personne.objects.all().
                order_by('-date_creation')]

        total = Personne.objects.all().count()
        total_new = len(new_people_registered)
        if total_new > 50:
            append_m(str(_("Since the previous newsletter:")))
            if first_time:
                append_m(
                    msg=str(_("{} people are already "
                              "registered!").format(total)),
                    html_msg=str(_("<b>{}</b> people are "
                                   "already registered!").format(total))
                )
            else:
                append_m(
                    msg=str(
                        _("There have been {} new people registered!\n"
                          "There's a total of <b>{}</b> "
                          "people registered!").format(total_new, total)),
                    html_msg=str(
                        _("There have been <b>{}</b> new people registered!"
                          "<br/>"
                          "There's a total of <b>{}</b> "
                          "people registered!").format(total_new, total))
                )
            append_m(str(
                _("There's a total of <b>{}</b> travels!\n").format(
                    PersonneTravel.objects.filter(
                        date_v_fin__isnull=True).count())
            ))

            if total_new > 50:
                new_people_registered = new_people_registered[:50]
            # get UNIQUE "base" google maps ids:
            gmaps_ids = set([t.travel.tag_google_maps.id
                             for t in PersonneTravel.objects.filter(
                                 personne__in=new_people_registered)])
            gmaps_ids_left = deepcopy(gmaps_ids)
            # try to translate them:
            new_travels = []
            for gmaps_id in gmaps_ids:
                u = TagGoogleMapsTraduit.objects.filter(
                    tag_google_maps__pk=gmaps_id,
                    langue__locale__exact=personne.site_language.locale
                )
                if len(u):  # found in his/her language -> add:
                    gmaps_ids_left.remove(gmaps_id)
                    new_travels.append(u[0])
            # if not enough new travels, let's add some NOT translated ones:
            if len(new_travels) < 10:
                for gmaps_id in gmaps_ids_left:
                    # just get the first translation:
                    u = TagGoogleMapsTraduit.objects.filter(
                        tag_google_maps__pk=gmaps_id
                    )
                    if len(u):  # add the first one, even if not translated:
                        new_travels.append(u[0])

            # 15 random travels max.
            append_m(str(_("Here are some new travels that have been added:")),
                     with_newline=True)
            # for travel in random.sample(new_travels, min(15, len(new_travels))):
            #     append_m(u'- {}'.format(travel.formatted_address),
            #              with_newline=False)
            # append_m(u'\n', with_newline=False)
            for travel in random.sample(new_travels, min(15, len(new_travels))):
                append_m('- {}'.format(travel.formatted_address),
                         with_newline=True)

        # ------------------
        # searches! Show the 10 "random" searches of the language of the user
        # get UNIQUE "base" google maps ids:
        gmaps_ids = [
            ps.search.tag_google_maps.id
            for ps in PersonneSearch.objects.filter(
                Q(search__langue__locale__exact=personne.site_language.locale) &
                ~Q(personne=personne)).
            distinct().
            order_by('-date_creation')]
        if len(gmaps_ids) > 200:
            n = 1000
            ok = set(gmaps_ids[:n])
            while len(ok) > 200:
                n -= 1
                ok = set(gmaps_ids[:n])
            gmaps_ids = ok
        else:
            gmaps_ids = set(gmaps_ids)

        gmaps_ids_final = []
        for g_id in gmaps_ids:
            a = PersonneTravel.objects.filter(travel__tag_google_maps__pk=g_id)
            if a.count() > 39:
                gmaps_ids_final.append((g_id, a.count(),))
        total = len(gmaps_ids_final)
        if total > 10:  # min. 10 searches (should be always more!)
            append_m(str(_("Here are some travels searches "
                           "that have been done:")),
                     with_newline=False)
            # 10 random searches max.
            for gmaps_id, cnt in random.sample(gmaps_ids_final, min(20, total)):
                # no safety check: we always get a translation (query gmaps_ids)
                search_travel = TagGoogleMapsTraduit.objects.filter(
                    tag_google_maps__exact=gmaps_id,
                    langue__locale__exact=personne.site_language.locale
                )[0]
                append_m(str(_('- {} ({} results)')).format(
                    search_travel.formatted_address,
                    cnt),
                    html_msg=str(_('- <a href="{}?travel={}" target="_blank">'
                                   '{}'
                                   '</a>'
                                   ' ({} results)')).format(
                        "{}{}".format(personne.site_web,
                                       reverse('my_home_search')
                                       ).replace('http://', 'https://'),
                        six.moves.urllib.parse.quote_plus(
                            search_travel.formatted_address.encode('utf8')
                        ),
                        search_travel.formatted_address,
                        cnt),
                    with_newline=False
                )
            append_m('\n', with_newline=False)

        # ------------------
        # there should be always something to send, but just in case:
        mail_is_sent = False
        if len(message) > 2:

            # ------------------
            # message d'invite pour se connecter :
            append_m(
                str(_('If you would like to find out more, '
                      'please log in via the following link:')),
                with_newline=False)
            append_m(
                "{}{}".format(personne.site_web, reverse('my_home_index'))
            )

            # ------------------
            # message pour modifier l'abonnement :
            append_m(
                str(_('If you no longer wish to receive '
                      'the Cogoflyer dashboard, '
                      'or any other notifications, '
                      'please click here:')),
                with_newline=False)
            append_m("{}{}".format(
                personne.site_web, reverse('my_home_profile_edit'))
            )
            append_m(
                str(_("And don't forget to click on: 'Change my parameters'"))
            )
            # output for me, with removing all double "\n"
            print(re.sub('\n+', '\n',
                         "\n".join([personne.user.email, ] + message)))
            send_mail(
                subject=_("Cogofly's news"),
                message="\n".join(message).encode('utf-8'),
                html_message="<br/>\n".join(html_message).encode('utf-8'),
                from_email='newsletter@cogofly.com',
                recipient_list=[personne.user.email, ])
            # send a copy every 200 mails:
            if (nb_mails_sent % 200) == 0:
                send_mail(
                    subject=' '.join(["Cogofly's news envoyées à : ",
                                       personne.user.email]).encode('utf-8'),
                    message="\n".join([personne.user.email, ] +
                                       message).encode('utf-8'),
                    html_message="<br/>\n".join([personne.user.email, ] +
                                                 html_message).encode('utf-8'),
                    from_email='contact@cogofly.com',
                    recipient_list=['cogofly+news@gmail.com', ])
            mail_is_sent = True

            # (!) only save if production mode:
            import cogofly.settings
            if not cogofly.settings.DEBUG and not fake:
                # ok, sent -> remember it in the database:
                d = make_aware(django_datetime.now())
                for activite in activites:
                    n = PersonneActiviteNewsletter.objects.create(
                        activite=activite, personne=personne, date_sent=d
                    )
                    n.save()
                for blog in blogs_to_send:
                    n = PersonneBlogNewsletter.objects.create(
                        blog=blog.blog, personne=personne, date_sent=d
                    )
                    n.save()

                personne.newsletter_date_sent = d
                personne.save()
                a = random.randint(2, 5)
                print(('Mail sent at {}'.format(d)))
                print(('Sleeping {} s...'.format(a)))
                time.sleep(a)

        translation.deactivate()
        return mail_is_sent

    def handle(self, *args, **options):
        if options['reset_all_news']:
            try:
                reset = bool(options['reset_all_news'])
                if reset:
                    Personne.objects\
                        .filter(est_detruit__isnull=True,
                                date_v_fin__isnull=True,
                                est_active__exact=True)\
                        .update(newsletter_date_sent=None)
                    self.stdout.write("Successfully reset all active accounts")
            except ValueError:
                raise CommandError('reset_all_news has to be a boolean')

        elif options['reset_personne_id']:
            try:
                personne_id = int(options['reset_all_news'])
            except ValueError:
                raise CommandError('reset_personne_id has to be an integer')

            try:
                p = Personne.objects.get(pk=personne_id)
                p.newsletter_date_sent = None
                p.save()
                self.stdout.write("Successfully "
                                  "reset person n.{}".format(personne_id))
            except Personne.DoesNotExist:
                raise CommandError('Personne {} not found'.format(personne_id))

        else:
            d = make_aware(django_datetime.now())
            fake = options.get('fake', False)
            if fake:
                q_filter = Q(id__exact=585)  # Olivier Pons / 613: Olivier Dofus
            else:
                q_filter = (
                    # ! compare : "date_sent < (now minus *2* days)" not "1 day"
                    Q(newsletter_date_sent__isnull=True) |
                    (
                        (Q(newsletter_configuration__exact=
                           PersonneEnums.NEWSLETTER_CONFIGURATION_EVERY_DAY) |
                         Q(newsletter_configuration__isnull=True)) &
                        Q(newsletter_date_sent__lte=d - timedelta(days=2))
                    ) |
                    (
                        Q(newsletter_configuration__exact=
                          PersonneEnums.NEWSLETTER_CONFIGURATION_EVERY_WEEK) &
                        Q(newsletter_date_sent__lte=d - timedelta(days=8))
                    ) |
                    (
                        Q(newsletter_configuration__exact=
                          PersonneEnums.NEWSLETTER_CONFIGURATION_EVERY_MONTH) &
                        Q(newsletter_date_sent__lte=d - timedelta(days=31))
                    )
                )
            personnes_to_send = Personne.objects.filter(
                Q(est_detruit__isnull=True,
                  date_v_fin__isnull=True,
                  est_active__exact=True)
                & q_filter
            )
            nb_mails_sent = 0
            for personne in personnes_to_send:
                print(str(personne))

                # (!) newly registered = wait 2 days before sending:
                if personne.newsletter_date_sent is None:
                    if personne.date_creation < (d - timedelta(days=2)):
                        continue
                if self.send_newsletter(personne, nb_mails_sent, fake):
                    nb_mails_sent += 1
            # (!) dont use self.stdout.write(), not available here, just print:
            print('Successfully sent newsletters')
