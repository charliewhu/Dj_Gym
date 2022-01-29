from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Gender, TrainingFocus, User, UserProfile, UserRM


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Gender)
admin.site.register(TrainingFocus)
admin.site.register(UserRM)


