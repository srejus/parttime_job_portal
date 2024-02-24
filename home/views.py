from django.shortcuts import render,redirect
from django.views import View

from jobs.models import JobListing
from accounts.models import Account

# Create your views here.
class IndexView(View):
    def get(self,request):
        jobs = JobListing.objects.all().order_by('-id')
        msg = request.GET.get("msg")
        if request.user.is_authenticated:
            acc = Account.objects.get(user=request.user)
            if acc.user_type == 'COMPANY':
                return redirect("/hr/")
        return render(request,'index.html',{'jobs':jobs,'msg':msg})
