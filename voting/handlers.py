from rapidsms.contrib.handlers import KeywordHandler
from django.db.models import F

from .models import Choice


class ResultHandler(KeywordHandler):
    keyword = 'results'

    def help(self):
        parts = []
        for choice in Choice.objects.all():
            part = "%s: %d" % (choice.name, choice.votes)
            parts.append(part)

        msg = "; ".join(parts)
        self.respond(msg)

    def handle(self, text):
        self.help()


class VoteHandler(KeywordHandler):
    keyword = 'vote'

    def help(self):
        choices = "|".join(Choice.objects.values_list('name', flat=True))
        self.respond("Valid Commands: VOTE <%s>" % choices)

    def handle(self, text):
        try:
            choice = Choice.objects.get(name__iexact=text)
            choice.votes += 1
            choice.save(update_fields=['votes'])
            self.respond("Your vote for %s has been counted" % text)
        except Choice.DoesNotExist:
            self.help()
