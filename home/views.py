from django.shortcuts import render,redirect
from django.views import View

from jobs.models import JobListing


# Create your views here.
class IndexView(View):
    def get(self,request):
        jobs = JobListing.objects.all().order_by('-id')
        msg = request.GET.get("msg")
        return render(request,'index.html',{'jobs':jobs,'msg':msg})
