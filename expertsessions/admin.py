from django.contrib import admin
from .models import Languages, Sessiondurations, Timeslots, Availabletimes, Expertsessions

#@admin.register(Languages)
#class LanguageAdmin(admin.ModelAdmin):
    #list_display = ('language_code',)
    #search_fields = ('language_code',)
    #ordering = ('language_code',)
    #list_filter = ('language_code',)


#@admin.register(Sessiondurations)
#class SessiondurationsAdmin(admin.ModelAdmin):
    #list_display = ('duration',)
    #search_fields = ('duration',)
    #ordering = ('duration',)
    #list_filter = ('duration',)


#@admin.register(Timeslots)
#class TimeslotsAdmin(admin.ModelAdmin):
    #list_display = ('start_time', 'end_time')
    #search_fields = ('start_time', 'end_time')
    #ordering = ('start_time',)
    #list_filter = ('start_time', 'end_time',)


#@admin.register(Availabletimes)
#class AvailabletimesAdmin(admin.ModelAdmin):
    #list_display = ('day_of_week', 'timeslot') 
    #search_fields = ('day_of_week', 'timeslot__start_time', 'timeslot__end_time') 
    #ordering = ('day_of_week',)  # إزالة expert
    #list_filter = ('day_of_week', 'timeslot',) 



@admin.register(Expertsessions)
class ExpertsessionsAdmin(admin.ModelAdmin):
    list_display = (
        'expert_name', 
        'session_price',
        
        'sessionduration_list',
        'languages_list',
        'is_deleted',
    )
    search_fields = ('expert__name_ar', 'expert__name_en', 'details',) 
    list_filter = ('expert', 'session_price', 'is_deleted', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    filter_horizontal = ('availabletimes', 'sessionduration','languages')

    def availabletimes_list(self, obj):
        return ", ".join([str(at.timeslot) for at in obj.availabletimes.all()])
    
    availabletimes_list.short_description = 'Available Times'

    def sessionduration_list(self, obj):
        return ", ".join([str(duration.duration) for duration in obj.sessionduration.all()])
    
    sessionduration_list.short_description = 'Session Durations'

    def languages_list(self, obj):
        return ", ".join([str(language_code.language_code) for language_code in obj.languages.all()])
    
    languages_list.short_description = 'Languages'

    def expert_name(self, obj):
        return obj.expert.name_ar 
    
    expert_name.short_description = 'Expert Name'

    fieldsets = (
        (None, {
            'fields': ('expert', 'session_price', 'availabletimes', 'sessionduration','languages', 'details', 'is_deleted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
