from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Customusers

# استيراد الموديلات اللي هنخفيها من الواجهة
from social_django.models import Association, Nonce, UserSocialAuth
from expertsessions.models import Languages, Timeslots, Sessiondurations, Availabletimes

# إلغاء تسجيلهم من الـ admin panel
for model in [Association, Nonce, UserSocialAuth, Languages, Timeslots, Sessiondurations, Availabletimes]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass


class CustomusersAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('User Type'), {'fields': ('user_type',)}),
        (_('Profile Image'), {'fields': ('file',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'file'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


# تسجيل المستخدمين المخصصين في لوحة الإدارة
admin.site.register(Customusers, CustomusersAdmin)

# تخصيص شكل لوحة التحكم
admin.site.site_title = _("Site administration")
admin.site.site_header = _("Custom Users Administration")
admin.site.index_title = _("Welcome to the Custom Users Admin")
