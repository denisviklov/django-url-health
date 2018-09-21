import string
import random

from django.db import models


class LinkStore(models.Model):
    link = models.URLField()
    description = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(default=0, blank=True)


class Scanning(models.Model):
    STOP, RUN = range(2)
    STATUSES = (
        (STOP, 'Stop'),
        (RUN, 'Run')
        )

    status = models.IntegerField(choices=STATUSES, default=STOP)
    timestamp = models.DateTimeField(auto_now=True)


class TokenStore(models.Model):
    token = models.CharField(max_length=128, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def _generate_token(self):
        symbols = '{0}{1}'.format(string.ascii_letters, string.digits)
        token = ''

        for _ in range(127):
            token.join(random.choice(symbols))

        return token

    def save(self, *args, **kwargs):
        self.token = self._generate_token()
        super().save(*args, **kwargs)
