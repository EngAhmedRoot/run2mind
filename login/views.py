from django.shortcuts import render, redirect
from django.views.generic.base import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, PatientsignupForm
from customusers.models import Customusers
from patients.models import Patients




class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login/login.html', context={"login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            print(login_form.cleaned_data["username"])   
            print(login_form.cleaned_data["password"])         
            user = authenticate(username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"])
            if user is not None and user.is_active:
                login(request, user)
                print(f"User {user.username} logged in as {user.user_type}")
                
                if user.is_superuser or user.is_staff:
                    return redirect("dashboard:list") 
                elif user.user_type == 'admin':
                    return redirect("dashboard:list") 
                elif user.user_type == 'expert':
                    return redirect("dashboard:list") 
                elif user.user_type == 'patient':
                    return redirect("dashboard:list") 
                else:
                    return redirect("dashboard:list") 


        return render(request, 'login/login.html', context={"login_form": login_form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login:login')




class PatientsignupView(View):
    def get(self, request):
        form = PatientsignupForm()
        return render(request, 'login/patientsignup.html', {'form': form})

    def post(self, request):
        form = PatientsignupForm(request.POST)
        
        # Debug: عرض البيانات المستقبلة من الفورم
        print("POST Data:", request.POST)

        if form.is_valid():
            print("Form is valid")  # Debug: التحقق من صحة الفورم
            
            try:
                # إنشاء المستخدم مع التأكد من استخدام البريد الإلكتروني كـ username
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # التحقق من أن البريد الإلكتروني غير مكرر
                if Customusers.objects.filter(username=email).exists():
                    form.add_error('username', 'This email is already taken.')
                    return render(request, 'login/patientsignup.html', {'form': form})

                user = Customusers.objects.create(
                    username=email,
                    password=make_password(password),
                    email=email,
                    user_type='patient',
                )
                print("User created:", user)  # Debug: تأكيد إنشاء المستخدم
                
                # إضافة المستخدم إلى جروب Patient-Group
                try:
                    patient_group = Group.objects.get(name="Patient-Group")
                    user.groups.add(patient_group)
                    print(f"User added to group: {patient_group.name}")  # Debug: تأكيد الإضافة للجروب
                except Group.DoesNotExist:
                    print("Patient-Group does not exist.")  # Debug: في حالة عدم وجود الجروب
                
                # ربطه بالمريض
                patient = Patients.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    gender=form.cleaned_data['gender'],
                    birthdate=form.cleaned_data['birthdate'],
                )
                print("Patient created:", patient)  # Debug: تأكيد إنشاء المريض

                # تسجيل الدخول تلقائيًا
                login(request, user)
                print("User logged in")  # Debug: تأكيد تسجيل الدخول

                # إعادة التوجيه
                return redirect('dashboard:list')  # تعديل الوجهة حسب الحاجة
            except Exception as e:
                print("Error occurred:", e)  # Debug: عرض الأخطاء في حالة وجود مشكلة
                form.add_error(None, "An error occurred while processing your request.")
        else:
            print("Form is not valid")  # Debug: إذا كان الفورم غير صالح
            print(form.errors)  # Debug: عرض الأخطاء
        
        # إذا كان هناك أخطاء، إعادة عرض الصفحة مع الأخطاء
        return render(request, 'login/patientsignup.html', {'form': form})

