from django.contrib import admin
from accounts.models import FrequencyAllocation, Gender, TrainingFocus, Split, SplitDay, SplitDayForce, SplitItem, User


admin.site.register(User)
# admin.site.register(UserProfile)
admin.site.register(Gender)
admin.site.register(TrainingFocus)
admin.site.register(Split)
admin.site.register(SplitItem)
admin.site.register(SplitDay)
admin.site.register(SplitDayForce)
admin.site.register(FrequencyAllocation)




