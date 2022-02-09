import datetime
from django.db import models
from django.db.models.aggregates import Avg, StdDev, Sum


class ReadinessAnswerManager(models.Manager):
    
    def mean(self, user):
        """We want the User's mean total readiness in the last 40 instances"""
        m = super().get_queryset()\
            .filter(readiness__user=user)\
            .order_by('-readiness')[:40]\
            .values('readiness')\
            .annotate(sum = Sum('rating'))\
            .aggregate(Avg('sum'))

        return m.get('sum__avg', None)

    def stddev(self, user):
        """We want the User's stddev for total readiness in the last 40 instances"""
        s = super().get_queryset()\
            .filter(readiness__user=user)\
            .order_by('-readiness')[:40]\
            .values('readiness')\
            .annotate(sum = Sum('rating'))\
            .aggregate(StdDev('sum'))

        s = s.get('sum__stddev', None)

        try: 
            s = round(s, 2)
        except:
            s
        
        return s

