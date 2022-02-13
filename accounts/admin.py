from django.contrib import admin
from accounts.models import FrequencyAllocation, Gender, TrainingFocus, TrainingSplit, User, UserProfile


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Gender)
admin.site.register(TrainingFocus)
admin.site.register(TrainingSplit)
admin.site.register(FrequencyAllocation)




