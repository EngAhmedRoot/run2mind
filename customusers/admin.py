from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Customusers

class CustomusersAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('User Type'), {'fields': ('user_type',)}),
        (_('Profile Image'), {'fields': ('file',)}),
    )

    # تخصيص الحقول عند إضافة مستخدم جديد
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type','file'),
        }),
    )

    # تخصيص الأعمدة المعروضة في قائمة المستخدمين
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type')

    # تخصيص الحقول التي يمكن البحث فيها
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # تخصيص ترتيب المستخدمين في القائمة
    ordering = ('username',)


# تسجيل النموذج في لوحة الإدارة
admin.site.register(Customusers, CustomusersAdmin)

# تخصيص عنوان الموقع في لوحة الإدارة
admin.site.site_title = _("Site administration")
admin.site.site_header = _("Custom Users Administration")
admin.site.index_title = _("Welcome to the Custom Users Admin")
