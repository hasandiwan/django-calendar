import datetime

from django.db import models
from django.db.utils import IntegrityError
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200, null=True)
    team_one = models.CharField(max_length=250, null=True)
    team_two = models.CharField(max_length=250, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.TextField(null=True)

    @property
    def get_html_url(self):
        url = reverse("cal:event_edit", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    def save(self):
        try:
            super().save()
        except IntegrityError:
            self.end_time = self.start_time + datetime.timedelta(minutes=90)
            super().save()
