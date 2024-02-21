from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from hr.models import Company

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
