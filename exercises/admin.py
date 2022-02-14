from ast import For
from django.contrib import admin
from .models import Exercise, Force, ForceCategory, Mechanic, MuscleGroup, Progression, ProgressionType, ProgressionTypeAllocation, Purpose, Tier, UserRM

admin.site.register(UserRM)
admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Force)
admin.site.register(ForceCategory)
admin.site.register(Tier)
admin.site.register(Purpose)
admin.site.register(Mechanic)
admin.site.register(ProgressionType)
admin.site.register(ProgressionTypeAllocation)
admin.site.register(Progression)

