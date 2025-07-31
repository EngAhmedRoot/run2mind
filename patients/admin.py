from django.contrib import admin
from django import forms
from .models import Patients
from customusers.models import Customusers

class PatientsAdmin(admin.ModelAdmin):
    # Correct field names for list_display
    list_display = ('name', 'file_no', 'job', 'gender', 'phone', 'mobile', 'email', 'created_at', 'is_deleted')

    # Correct ordering fields
    ordering = ('-created_at', 'file_no')

    # Searchable fields
    search_fields = ('name', 'file_no', 'job', 'phone', 'mobile', 'email', 'details')

    # Sidebar filters
    list_filter = ('gender', 'is_deleted', 'created_at')

    # Fields to display in the detail/edit view
    fieldsets = (
        (None, {
            'fields': ('user', 'file_no', 'name', 'birthdate', 'phone', 'mobile', 'email', 'gender', 'file')
        }),
        ('Professional Details', {
            'fields': ('job', 'details')
        }),
        ('Administrative', {
            'fields': ('is_deleted',),
        }),
    )

    # Custom form to display a date input widget for birthdate
    class PatientForm(forms.ModelForm):
        class Meta:
            model = Patients
            fields = '__all__'

        birthdate = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'YYYY-MM-DD',
                }
            )
        )

    form = PatientForm

    # Custom actions in the admin list view
    actions = ['mark_as_deleted', 'restore_deleted']

    # Action to mark patients as deleted
    def mark_as_deleted(self, request, queryset):
        queryset.update(is_deleted=True)
    mark_as_deleted.short_description = "Mark selected patients as deleted"

    # Action to restore deleted patients
    def restore_deleted(self, request, queryset):
        queryset.update(is_deleted=False)
    restore_deleted.short_description = "Restore selected patients"

    # Customizing the default queryset to exclude deleted patients
    def get_queryset(self, request):
        """Show only non-deleted patients by default."""
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)

    # Customize the 'user' field dropdown to show only users with type 'patient'
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Customusers.objects.filter(user_type='patient')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Patients, PatientsAdmin)
