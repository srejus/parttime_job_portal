from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from hr.models import Company,Attendence
from jobs.models import JobApplication


# getting attendence
from django.utils import timezone
from datetime import datetime

# Create your views here.

class LoginView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'login.html',{'err':err})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            acc = Account.objects.get(user=request.user)
            if acc.user_type == 'COMPANY':
                return redirect("/hr/")
            return redirect("/")
        err = "Invalid credentails!"
        return redirect(f"/account/login/?err={err}")
    

class SignupView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'signup.html',{'err':err})
    
    def post(self,request):
        username = request.POST.get("username")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")
        profile_pic = request.FILES.get("profile_pic")
        full_name = request.POST.get("full_name")
        number = request.POST.get("phone")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        resume = request.FILES.get("resume")
        location = request.POST.get("location")
        user_type = request.POST.get("user_type")

        company_name = request.POST.get("company_name")
        company_desc = request.POST.get("company_desc")
        company_logo = request.FILES.get("company_logo")

        if password1 != password2:
            err = "Password not matching!"
            return redirect(f"/accounts/signup?err={err}")
    
        user = User.objects.filter(username=username)
        if user.exists():
            err = "User with this username already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        acc = Account.objects.filter(Q(email=email) | Q(phone=number)).exists()
        if acc:
            err = "User with this phone or email already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        user = User.objects.create_user(username=username,email=email,password=password1)
        acc = Account.objects.create(user=user,full_name=full_name,
                                     phone=number, email=email,resume=resume,
                                     profile_pic=profile_pic,gender=gender,user_type=user_type)


        # saving company Instance
        Company.objects.create(user=acc,company_name=company_name,
                                         desc=company_desc,company_logo=company_logo)

        return redirect('/accounts/login')


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/")
    

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get_profile_completion(self,acc):
        percent = 0
        if acc.email:
            percent += 20
        if acc.phone:
            percent += 20
        if acc.qualification:
            percent += 20
        if acc.resume:
            percent += 20
        if acc.profile_pic:
            percent += 20 

        acc.profile_completion_percentage = percent
        acc.save()
        print("Percentage : ",percent)
        return percent
    
    def get(self,request,id=None):
        if id:
            acc = Account.objects.get(id=id)
        else:
            acc = Account.objects.get(user=request.user)
        skill = request.GET.get('skill')
        print('Skill : ',skill,request.GET.keys())
        if skill:
            skill_obj = PreferredSkills.objects.filter(user=acc,skill=skill)
            if not skill_obj.exists():
                PreferredSkills.objects.create(user=acc,skill=skill)
        percent = self.get_profile_completion(acc)
        jobs = JobApplication.objects.filter(applied_by=acc).order_by('-id')
        try:
            rating = Company.objects.get(user=acc).avg_rating
        except:
            rating = 0.0

        skills = PreferredSkills.objects.filter(user=acc)
        if  id:
            return render(request,'view_profile_company.html',{'acc':acc,'jobs':jobs,'rating':rating,'percent':percent,'skills':skills})


        # Assuming today's date
        current_date = timezone.now()

        attendence = Attendence.objects.filter(
            created_at__month=current_date.month,
            created_at__year=current_date.year
        ).count()
        return render(request,'profile.html',{'acc':acc,'jobs':jobs,'rating':rating,'percent':percent,'skills':skills,'attendence':attendence})
    
    def post(self,request):
        profile_pic = request.FILES.get("profile_pic")
        full_name = request.POST.get("full_name")
        number = request.POST.get("phone")
        email = request.POST.get("email")
        resume = request.FILES.get("resume")
        qualification = request.POST.get("qualification")
        location = request.POST.get("location")

        company_name = request.POST.get("company_name")
        company_desc = request.POST.get("company_desc")
        company_logo = request.FILES.get("company_logo")

        acc = Account.objects.get(user=request.user)

        if profile_pic:
            acc.profile_pic = profile_pic
        acc.full_name = full_name
        acc.email = email
        acc.phone = number
        acc.qualification = qualification
        acc.location=location
        if resume:
            acc.resume = resume
        if acc.user_type == 'COMPANY':
            company = Company.objects.get(user=acc)
            company.company_name = company_name
            if company_logo:
                company.company_logo = company_logo
            company.desc = company_desc
            company.save()
        
        acc.save()
        return redirect("/accounts/profile")


class DeleteSkillView(View):
    def get(self,request,id):
        PreferredSkills.objects.get(id=id).delete()
        return redirect("/accounts/profile")
    

@method_decorator(login_required,name='dispatch')
class MyJobView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        current_date = timezone.now()

        attendence = Attendence.objects.filter(
            created_at__month=current_date.month,
            created_at__year=current_date.year
        ).count()
        return render(request,'my_job.html',{'acc':acc,'attendence':attendence})