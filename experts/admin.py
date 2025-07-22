from django.contrib import admin
from django import forms
from .models import Experts
from customusers.models import Customusers

class ExpertsAdmin(admin.ModelAdmin):
    # تخصيص الأعمدة التي تظهر في قائمة الخبراء
    list_display = ('name_en', 'name_ar', 'specialization_en', 'specialization_ar', 'gender', 'experience_years', 'created_at', 'is_deleted')
    
    # تخصيص الأعمدة القابلة للفرز
    ordering = ('-created_at', 'name_en', 'experience_years')
    
    # تخصيص الحقول القابلة للبحث
    search_fields = ('name_en', 'name_ar', 'specialization_en', 'specialization_ar', 'email', 'phone')

    # تخصيص الفلاتر الجانبية
    list_filter = ('gender', 'experience_years',  'is_deleted', 'created_at')

    # الحقول التي تظهر عند عرض التفاصيل أو تعديل خبير
    fieldsets = (
        (None, {
            'fields': ('user', 'name_en', 'name_ar', 'birthdate', 'phone', 'email', 'gender', 'file')
        }),
        ('Professional Details', {
            'fields': ('specialization_en', 'specialization_ar', 'experience_years', 'certificates_en', 'certificates_ar', 'details_en', 'details_ar' )
        }),
        ('Administrative', {
            'fields': ('is_deleted',),  # فقط الحقول القابلة للتحرير
        }),
    )

    # تخصيص الـ form لعرض حقل birthdate بشكل مخصص
    class ExpertForm(forms.ModelForm):
        class Meta:
            model = Experts
            fields = '__all__'

        birthdate = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    'type': 'date', 
                    'placeholder': 'YYYY-MM-DD', 
                }
            )
        )

    form = ExpertForm


    # أزرار إضافية في صفحة القائمة
    actions = ['mark_as_deleted', 'restore_deleted']

    # دالة لتغيير حالة الحذف
    def mark_as_deleted(self, request, queryset):
        queryset.update(is_deleted=True)
    mark_as_deleted.short_description = "Mark selected experts as deleted"

    def restore_deleted(self, request, queryset):
        queryset.update(is_deleted=False)
    restore_deleted.short_description = "Restore selected experts"

    # تخصيص العناوين
    def get_queryset(self, request):
        """عرض العناصر غير المحذوفة فقط بشكل افتراضي."""
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)

    # تخصيص الـ dropdown لـ 'user' ليظهر فقط المستخدمين من نوع 'expert'
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Customusers.objects.filter(user_type='expert')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Experts, ExpertsAdmin)

