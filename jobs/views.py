from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *

# Create your views here.
class FetchJobView(View):
    def get(self,request,id=None):
        jobs = JobListing.objects.get(id=id)
        return render(request,'')
    
    def post(self,request):
        keyword = request.POST.get("keyword")
        location = request.POST.get("location")
        shift_type = request.POST.get("shift_type")
        jobs = JobListing.objects.filter(title__icontains=keyword,
                                         location__icontains=location,shift_type=shift_type).order_by('-id')
        
        return render(request,'/',{'jobs':jobs,'job':True})
    

@method_decorator(login_required, name='dispatch')
class ApplyJobView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'JOB_SEEKER':
            msg = "Company Cant Apply to a Job!"
            return redirect(f"/?msg={msg}")
    
        if acc.profile_completion_percentage < 80:
            msg = "You must complete your profile atleast 80% to apply for a job!"
            return redirect(f"/?msg={msg}")
        
        job = JobListing.objects.filter(id=id).first()
        job_application = JobApplication.objects.filter(job=job,applied_by=acc)
        if job_application.exists():
            msg = "You already applied to this Job!"
            return redirect(f"/?msg={msg}")
        
        JobApplication.objects.create(job=job,applied_by=acc)
        # send email noti to job provider

        msg = "Job applied Successfully!"
        return redirect(f"/?msg={msg}")


@method_decorator(login_required, name='dispatch')
class DeleteApplicationView(View):
    def get(self,request,id=None):
        job = JobApplication.objects.get(id=id)
        job.delete()
        return redirect("/accounts/profile")
