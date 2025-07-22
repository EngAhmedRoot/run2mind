
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, timedelta
from collections import defaultdict

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Expertsessions


class ExpertsessionsListView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    permission_required = 'experts.view_experts'
    model = Expertsessions
    context_object_name = 'expertsessions'
    template_name = 'expertsessions/expertsessions_list.html'

    def get_queryset(self):
        user = self.request.user

        # تحديد القيم الأساسية بناءً على نوع المستخدم
        if user.is_superuser or user.is_staff:
            queryset = Expertsessions.objects.all()
        elif user.user_type == 'admin':
            queryset = Expertsessions.objects.all()
        elif user.user_type == 'expert':
            #queryset = Expertsessions.objects.filter(expert__user=user, expert__user__is_active=True)
            queryset = Expertsessions.objects.all()
        elif user.user_type == 'patient':
            queryset = Expertsessions.objects.all() if user.is_active else Expertsessions.objects.none()
        else:
            queryset = Expertsessions.objects.all()

    
        # إضافة الفلاتر الأخرى
        name_filter = self.request.GET.get('name', '')
        if name_filter:
            queryset = queryset.filter(
                Q(expert__name_ar__icontains=name_filter) | Q(expert__name_en__icontains=name_filter)
            )

        gender_filter = self.request.GET.getlist('gender', [])
        if gender_filter:
            queryset = queryset.filter(expert__gender__in=gender_filter)

        language_filter = self.request.GET.getlist('language', [])
        if language_filter:
            queryset = queryset.filter(languages__language_code__in=language_filter)

        duration_filter = self.request.GET.getlist('duration', [])
        if duration_filter:
            queryset = queryset.filter(sessionduration__duration__in=duration_filter)

        # فلترة الأسعار
        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)
        if min_price and max_price:
            queryset = queryset.filter(session_price__gte=int(min_price), session_price__lte=int(max_price))


        today_filter = self.request.GET.get('today', '').lower() == 'true'
        emergency_filter = self.request.GET.get('emergency', '').lower() == 'true'
        now_time = datetime.now().time()
        end_time = (datetime.now() + timedelta(minutes=60)).time()
        today = datetime.today().strftime('%A')

        queryset = queryset.distinct().order_by('id')

        today_filter = self.request.GET.get('today', '').lower() == 'true'
        emergency_filter = self.request.GET.get('emergency', '').lower() == 'true'
    
        
        filtered_queryset = []
        
        for expertsession in queryset:
            # محاولة معرفة أقرب وقت متاح
            available_times = expertsession.availabletimes.select_related('timeslot').filter(
                Q(day_of_week=today) & Q(timeslot__start_time__gt=now_time)
            ).order_by('timeslot__start_time')
        
            if available_times.exists():
                expertsession.next_available_time = available_times.first().timeslot.start_time
                expertsession.next_time = expertsession.next_available_time
                expertsession.next_day = "Today"
            else:
                # البحث في المستقبل
                future_times = expertsession.availabletimes.select_related('timeslot').filter(
                    Q(timeslot__start_time__gt=now_time) | ~Q(day_of_week=today)
                ).order_by('day_of_week', 'timeslot__start_time')
        
                if future_times.exists():
                    expertsession.next_available_time = future_times.first().timeslot.start_time
                    expertsession.next_time = expertsession.next_available_time
                    expertsession.next_day = future_times.first().day_of_week
                else:
                    expertsession.next_time = None
                    expertsession.next_day = None
        
            # منطق الفلترة
            add_to_queryset = False
        
            if emergency_filter:
                emergency_available = expertsession.availabletimes.select_related('timeslot').filter(
                    Q(day_of_week=today) &
                    Q(timeslot__start_time__gte=now_time) &
                    Q(timeslot__start_time__lte=end_time)
                ).exists()
                if emergency_available:
                    add_to_queryset = True
        
            if today_filter:
                has_today_session = expertsession.availabletimes.select_related('timeslot').filter(
                    Q(day_of_week=today) & Q(timeslot__start_time__gt=now_time)
                ).exists()
                if has_today_session:
                    add_to_queryset = True
        
            if not today_filter and not emergency_filter:
                add_to_queryset = True
        
            if add_to_queryset:
                filtered_queryset.append(expertsession)
        
        return filtered_queryset

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def render_to_response(self, context, **response_kwargs):
        request = self.request
        page = request.GET.get('page', 1)
    
        queryset = self.get_queryset()
    
        paginate_by = 4  
    
        paginator = Paginator(queryset, paginate_by)
        page_obj = paginator.get_page(page)
    
        context['expertsessions'] = page_obj 
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
    
        current_page = page_obj.number
        total_pages = paginator.num_pages
    
        start_page = max(current_page - 1, 1)
        end_page = min(current_page + 1, total_pages)
    
        context['page_range'] = range(start_page, end_page + 1)
    
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                'expertsessions/_expertsessions_list_partial.html',
                context,
                request=request
            )
            return JsonResponse({'html': html})
    
        return super().render_to_response(context, **response_kwargs)
    




class ExpertsessionsDetailView(PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    permission_required = 'experts.view_experts'
    model = Expertsessions
    template_name = 'expertsessions/expertsessions_detail.html'

    def get_queryset(self):
        user = self.request.user

        # تحديد القيم الأساسية بناءً على نوع المستخدم
        if user.is_superuser or user.is_staff:
            queryset = Expertsessions.objects.all()
        elif user.user_type == 'admin':
            queryset = Expertsessions.objects.all()
        elif user.user_type == 'expert':
            queryset = Expertsessions.objects.all()
        elif user.user_type == 'patient':
            queryset = Expertsessions.objects.all() if user.is_active else Expertsessions.objects.none()
        else:
            queryset = Expertsessions.objects.none()

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expertsession = context['object']  # الحصول على الـ Expertsession الحالي

        # استرجاع الأوقات المتاحة
        available_times = expertsession.availabletimes.select_related('timeslot').all().order_by('timeslot__start_time')

        # تحديد الوقت المتاح التالي
        expertsession.next_available_time = available_times.first().timeslot.start_time if available_times.exists() else None

        # تحديد اليوم المتاح
        if expertsession.next_available_time:
            available_day = available_times.first().day_of_week
            today = datetime.today().strftime('%A')

            if available_day == today:
                expertsession.next_time = expertsession.next_available_time
                expertsession.next_day = "Today"
            else:
                expertsession.next_time = expertsession.next_available_time
                expertsession.next_day = f" {available_day}"

        # إضافة المواعيد القادمة والوقت المتاح في الـ context
        context['next_time'] = expertsession.next_time if hasattr(expertsession, 'next_time') else None
        context['next_day'] = expertsession.next_day if hasattr(expertsession, 'next_day') else None
        
        # إضافة جميع المواعيد المتاحة للـ expert
        context['available_times'] = available_times  # هذه هي جميع المواعيد المتاحة

        return context
