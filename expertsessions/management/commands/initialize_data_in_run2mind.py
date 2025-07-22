from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import Group, Permission
from datetime import time, datetime, timedelta
from expertsessions.models import Languages, Sessiondurations, Timeslots,  Availabletimes 


class Command(BaseCommand):
    help = 'Initialize data including groups, languages, time slots, and available times.'

    def handle(self, *args, **kwargs):
        self.create_groups_with_permissions()  # إنشاء المجموعات مع الصلاحيات
        self.create_languages()  # إنشاء اللغات
        self.create_session_durations()  # إنشاء فترات الجلسات
        self.create_timeslots()  # إنشاء الفترات الزمنية
        self.create_availabletimes()  # إنشاء الأوقات المتاحة

    def create_groups_with_permissions(self):
        groups = ['Admin-Group', 'Expert-Group', 'Patient-Group']
        created_count = 0  # عداد للمجموعات التي تم إنشاؤها

        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                created_count += 1
                print(f"Creating group: {group_name}")
            else:
                print(f"Group {group_name} already exists")
            
            # تخصيص الصلاحيات بناءً على اسم الجروب
            if group_name == 'Admin-Group':
                # إضافة كل الصلاحيات
                permissions = Permission.objects.all()
                group.permissions.add(*permissions)
            elif group_name in ['Expert-Group', 'Patient-Group']:
                # إضافة كل الصلاحيات ما عدا delete
                permissions = Permission.objects.exclude(codename__icontains='delete')
                group.permissions.add(*permissions)

        # طباعة النتيجة
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} groups and assigned permissions!'))




    def create_languages(self):
        # قائمة باللغات التي تريد إضافتها
        languages = [
            ('arabic', 'Arabic'),
            ('english', 'English'),
        ]

        created_count = 0  # عداد للغات التي تم إنشاؤها

        for code, name in languages:
            # تحقق إذا كانت اللغة موجودة بالفعل
            if not Languages.objects.filter(language_code=code).exists():
                # إضافة اللغة الجديدة
                Languages.objects.create(language_code=code)
                created_count += 1
                print(f"Creating language: {name}")
            else:
                print(f"Language {name} already exists")

        # طباعة النتيجة
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} languages!'))


    def create_session_durations(self):
        durations = [30, 60]  # فترات الجلسات المطلوبة (30 دقيقة و 60 دقيقة)

        for duration in durations:
            if not Sessiondurations.objects.filter(duration=duration).exists():
                Sessiondurations.objects.create(duration=duration)
                print(f"Creating session duration: {duration} minutes")
            else:
                print(f"Session duration {duration} minutes already exists")
    


    def create_timeslots(self):
        # بداية ونهاية اليوم
        start_time = time(0, 0)  # 12:00 AM
        end_time = time(23, 59)  # 11:59 PM
        timeslot_duration = 30  # المدة الزمنية بالـ minutes

        current_time = start_time
        created_count = 0  # عداد للفترات الزمنية التي تم إنشاؤها
        total_possible_slots = 24 * 60 // timeslot_duration  # إجمالي عدد الفترات الممكنة
        existing_timeslots = set(  # الحصول على جميع الفترات الزمنية الموجودة
            Timeslots.objects.values_list('start_time', 'end_time')
        )

        while current_time < end_time:
            # إذا أضفنا بالفعل جميع الفترات الممكنة، توقف
            if len(existing_timeslots) >= total_possible_slots:
                print("All possible timeslots have been created. Exiting.")
                break

            # حساب الوقت التالي
            next_time = (datetime.combine(datetime.min, current_time) + timedelta(minutes=timeslot_duration)).time()

            # تحقق إذا كانت الفترة الزمنية موجودة في مجموعة الفترات
            if (current_time, next_time) not in existing_timeslots:
                Timeslots.objects.create(start_time=current_time, end_time=next_time)
                created_count += 1
                print(f"Creating timeslot: {current_time} - {next_time}")
                # إضافة الفترة الجديدة إلى المجموعة
                existing_timeslots.add((current_time, next_time))
            else:
                print(f"Timeslot already exists: {current_time} - {next_time}")

            # تحديث الوقت الحالي
            current_time = next_time

        # طباعة النتيجة
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} time slots!'))

    def create_availabletimes(self):
        # تعريف أيام الأسبوع
        days_of_week = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        all_timeslots = Timeslots.objects.all()
        created_count = 0

        # البدء في إنشاء الأوقات المتاحة
        with transaction.atomic():
            for day in days_of_week:
                for timeslot in all_timeslots:
                    # تحقق إذا كانت الفترة الزمنية لهذا اليوم موجودة
                    if not Availabletimes.objects.filter(day_of_week=day, timeslot=timeslot).exists():
                        Availabletimes.objects.create(day_of_week=day, timeslot=timeslot)
                        created_count += 1
                        print(f"Creating available time: {day} - {timeslot}")

        # طباعة النتيجة
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} available times!'))
