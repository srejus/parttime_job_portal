from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from hr.models import Company
from jobs.models import JobApplication

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
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        jobs = JobApplication.objects.filter(applied_by=acc).order_by('-id')
        return render(request,'profile.html',{'acc':acc,'jobs':jobs})
    
    def post(self,request):
        profile_pic = request.FILES.get("profile_pic")
        full_name = request.POST.get("full_name")
        number = request.POST.get("phone")
        email = request.POST.get("email")
        resume = request.FILES.get("resume")

        company_name = request.POST.get("company_name")
        company_desc = request.POST.get("company_desc")
        company_logo = request.FILES.get("company_logo")

        acc = Account.objects.get(user=request.user)

        if profile_pic:
            acc.profile_pic = profile_pic
        acc.full_name = full_name
        acc.email = email
        acc.phone = number
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