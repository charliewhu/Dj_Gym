import datetime
from django.db import models
from django.db.models.aggregates import Avg, Sum


class ReadinessAnswerManager(models.Manager):
    
    def mean(self, user):
        """We want the User's mean total readiness in the last 40 instances"""
        m = super().get_queryset()\
            .filter(readiness__user=user)\
            .values('id')\
            .order_by('-id')[:40]\
            .annotate(sum = Sum('rating'))\
            .aggregate(Avg('sum'))

        return m.get('sum__avg', None)

