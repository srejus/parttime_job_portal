from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime

from .models import *
from jobs.models import *


# Create your views here.
@method_decorator(login_required, name='dispatch')
class HrHomeView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        return render(request,'hr_home.html')

@method_decorator(login_required, name='dispatch')
class HrJobView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        company = Company.objects.get(user__user=request.user)
        applications = JobApplication.objects.filter(job__posted_by_company=company).exclude(
            status__in=['REJECTED','ACCEPTED'])
        return render(request,'hr_job_applications.html',{'applications':applications})


@method_decorator(login_required, name='dispatch')
class HrEmployeeView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        company = Company.objects.get(user__user=request.user)
        employees = Employee.objects.filter(company=company)
        if id:
            employee = Employee.objects.filter(id=id).first()
            attendence = Attendence.objects.filter(created_at=datetime.today().date(),employee=employee).last()
            return render(request,'hr_view_employee.html',{'employee':employee,'attendence':attendence})
        return render(request,'hr_employees.html',{'employees':employees})
    

@method_decorator(login_required, name='dispatch')
class HrRemoveEmployeeView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        Employee.objects.filter(id=id).delete()
        return redirect("/hr")



@method_decorator(login_required, name='dispatch')
class MarkAttendence(View):
    def get(self,request,id):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        employeee = Employee.objects.get(id=id)
        company = Company.objects.get(user__user=request.user)
        if not  Attendence.objects.filter(employee=employeee,company=company,created_at=datetime.today().date()):
            Attendence.objects.create(employee=employeee,company=company)
        return redirect(f"/hr/employee/{id}")



@method_decorator(login_required, name='dispatch')
class PostJobView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            msg = "Only company can post a job!"
            return redirect(f"/?msg={msg}")
        
        return render(request,'post_job.html')
    
    def post(self,request):
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        sf = request.POST.get("s_f")
        st = request.POST.get("s_t")
        base = request.POST.get("base")
        pay_type = request.POST.get("pay_type")
        shift = request.POST.get("shift")
        location = request.POST.get("location")

        acc = Account.objects.get(user=request.user)
        company = Company.objects.get(user=acc)

        JobListing.objects.create(
            posted_by_company=company,title=title,desc=desc,
            salary_from=sf,salary_to=st,
            daily_salary=base,pay_type=pay_type,
            shift_type=shift,location=location
        )
        msg = "Job Posted Successfully!"
        return redirect(f"/?msg={msg}")
    

@method_decorator(login_required, name='dispatch')
class ApproveView(View):
    def get(self,request,id):
        job = JobApplication.objects.get(id=id)
        job.status = 'ACCEPTED'
        acc = job.applied_by
        acc.working_company_id = job.job.posted_by_company.id
        acc.save()
        job.save()


        # add that user to employee table and make the status of that employee to working at companyname
        if not Employee.objects.filter(employee=job.applied_by).exists():
            Employee.objects.create(employee=job.applied_by)
        return redirect("/hr/")


@method_decorator(login_required, name='dispatch')
class RejectView(View):
    def get(self,request,id):
        job = JobApplication.objects.get(id=id)
        job.status = 'REJECTED'
        job.save()
        return redirect("/hr/")