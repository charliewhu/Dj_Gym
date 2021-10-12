from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserGroup
from .forms import CustomUserCreationForm, CustomUserChangeForm



class UserGroupInline(admin.StackedInline):
    model = UserGroup.users.through


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [UserGroupInline]
    model = User
    list_display = ('email', 'is_admin', 'is_active', 'is_staff', 'last_login')
    search_fields = ('email',)
    list_filter = ('email', 'is_admin', 'is_active', 'is_staff', )

    #field appearing when changing a user
    fieldsets = ((None, {'fields': ('email', 'password', 'is_staff', 'is_admin', 'is_active', 'groups', 'profile_pic')}),
                 )

    #fields appearing when adding a new user
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_admin', 'is_active', 'profile_pic')}
         ),
    )

    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserGroup)
