import datetime
from django.db import models
from django.db.models.aggregates import Max

class UserRMManager(models.Manager):
    """We want the User's highest rep max, for specific Exercise, in the last 90 days"""
    def latest_one_rm(self, user, exercise):
        timeout = datetime.date.today() - datetime.timedelta(days=90)
        return \
            super()\
            .get_queryset()\
            .filter(user=user, exercise=exercise, date__gte=timeout)\
            .aggregate(Max('one_rep_max'))