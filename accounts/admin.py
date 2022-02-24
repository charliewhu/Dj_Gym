from django.contrib import admin
from accounts.models import FrequencyAllocation, Gender, TrainingFocus, Split, TrainingSplitDay, TrainingSplitDayForce, SplitItem, User


admin.site.register(User)
# admin.site.register(UserProfile)
admin.site.register(Gender)
admin.site.register(TrainingFocus)
admin.site.register(Split)
admin.site.register(SplitItem)
admin.site.register(TrainingSplitDay)
admin.site.register(TrainingSplitDayForce)
admin.site.register(FrequencyAllocation)




