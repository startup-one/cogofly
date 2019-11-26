
import datetime
from google.appengine._internal.django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to clean out old data from the database (only expired sessions at the moment)."

    def handle_noargs(self, **options):
        from google.appengine._internal.django.db import transaction
        from google.appengine._internal.django.contrib.sessions.models import Session
        Session.objects.filter(expire_date__lt=datetime.datetime.now()).delete()
        transaction.commit_unless_managed()
