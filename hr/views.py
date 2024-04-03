from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime

from .models import *
from jobs.models import *
from accounts.models import PreferredSkills
from project.utils import  send_mail
from home.models import Support

# Create your views here.
@method_decorator(login_required, name='dispatch')
class HrHomeView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        term = request.GET.get("term")
        location = request.POST.get("location")

        if term:
            skills = PreferredSkills.objects.filter(skill__icontains=term).values_list('user__id',flat=True)
            candidates = Account.objects.filter(user_type='JOB_SEEKER',id__in=skills)
            if location:
                print("Candidates")
                candidates = candidates.filter(location__icontains=location)
            
            print("candidates : ",candidates)
            return render(request,'hr_candidates.html',{'candidates':candidates})

        return render(request,'hr_home.html')

@method_decorator(login_required, name='dispatch')
class HrJobView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'COMPANY':
            return redirect("/")
        
        company = Company.objects.get(user__user=request.user)
        applications = JobApplication.objects.filter(job__posted_by_company=company).exclude(
            status__in=['REJECTED'])
        return render(request,'hr_job_applications.html',{'applications':applications})

from django.utils import timezone


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
            att = Attendence.objects.filter(employee=employee)
            try:
                current_date = timezone.now()

                # Filter attendances for the current month
                whole_attendence = Attendence.objects.filter(
                    created_at__year=current_date.year,
                    created_at__month=current_date.month
                )
                current_month_attendances = whole_attendence.filter(is_paid=False
                )

                whole_attendence = whole_attendence.count()
                current_month_attendances = current_month_attendances.count()
            except:
                current_month_attendances = 0
                whole_attendence = 0
            pay = current_month_attendances * employee.daily_pay
            msg = request.GET.get("msg")
            return render(request,'hr_view_employee.html',{'employee':employee,'attendence':attendence,
                                                           'current_month_attendances':whole_attendence,'pay':pay,'msg':msg})
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
    

@method_decorator(login_required,name='dispatch')
class HrJobsView(View):
    def get(self,request):
        company = Company.objects.filter(user__user=request.user).last()
        jobs = JobListing.objects.filter(posted_by_company=company)
        return render(request,'hr_jobs.html',{'jobs':jobs})


@method_decorator(login_required,name='dispatch')
class HrDeleteJobsView(View):
    def get(self,request,id):
        company = Company.objects.filter(user__user=request.user).last()
        jobs = JobListing.objects.filter(posted_by_company=company,id=id).delete()
        return redirect("/hr/my-jobs")



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

        int_at = request.GET.get("int_at")

        # schedule the interview for that time
        email_msg = f"Hello {acc.full_name},\n\nYour job application for the role {job.job.title} has been approved by the company and interview scheduled at {int_at}\n\n\nThanks"

        subject = f"Congratulations You Have Been Shortlisted for the role {job.job.title}"
        send_mail(acc.email,subject,email_msg)
        return redirect("/hr/")


class MarkAsEmployeeView(View):
    def get(self,request,id):
        job = JobApplication.objects.get(id=id)
        if not Employee.objects.filter(employee=job.applied_by).exists():
            Employee.objects.create(employee=job.applied_by,daily_pay=job.job.daily_salary,company=job.job.posted_by_company)
        return redirect("/hr/")

@method_decorator(login_required, name='dispatch')
class RejectView(View):
    def get(self,request,id):
        job = JobApplication.objects.get(id=id)
        job.status = 'REJECTED'
        job.save()
        return redirect("/hr/")
    

@method_decorator(login_required,name='dispatch')
class HrSalaryView(View):
    def get(self,request,id=None):
        current_date = timezone.now()
        Attendence.objects.filter(
                    created_at__year=current_date.year,
                    created_at__month=current_date.month,is_paid=False
                ).update(is_paid=True)
    
        msg = "Salary Paid Successfully!"

        # send noti if needed
        return redirect(f"/hr/employee/{id}?msg={msg}")
    

@method_decorator(login_required,name='dispatch')
class InterestedCandidateView(View):
    def get(self,request,id):
        usr = Account.objects.get(id=id)
        acc = Account.objects.get(user=request.user)
        company = Company.objects.filter(user=acc)
        if company.exists():
            company = company.last()
            subject = f"You got a Job Interest from {company.company_name}"
            msg = f"Hello {usr.full_name},\n{company.company_name} has shown interest on your profile.\nYou can apply to the company if you are interested\n\nThanks"

            send_mail(usr.email,subject,msg)

        return redirect("/hr/")
    

@method_decorator(login_required,name='dispatch')
class HrSupportView(View):
    def get(self,request):
        company = Company.objects.filter(user__user=request.user)
        if company.exists():
            company = company.last()
            tickets = Support.objects.filter(company=company).order_by('-id')
        else:
            tickets = []
        return render(request,'hr_support.html',{'tickets':tickets})