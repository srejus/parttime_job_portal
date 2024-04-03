from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Avg

from jobs.models import JobListing
from accounts.models import Account
from hr.models import Review,Company
from project.utils import send_mail
from .models import Support


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


@method_decorator(login_required, name='dispatch')
class AddReviewView(View):
    def get(self,request,id):
        return render(request,'add_review.html',{'id':id})

    def post(self,request,id):
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        
        acc = Account.objects.get(user=request.user)
        company = Company.objects.get(id=id)

        if not Review.objects.filter(user=acc,company=company).exists():
            Review.objects.create(user=acc,company=company,review=review,rating=rating)
            average_rating = round(Review.objects.filter(company=company).aggregate(avg_rating=Avg('rating'))['avg_rating'],1)
            company.avg_rating = average_rating
            company.save()

        return redirect("/accounts/profile")
    

class SupportView(View):
    def get(self,request):
        companies = Company.objects.all()
        return render(request,'support.html',{'companies':companies})
    

    def post(self,request):
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        com_id = request.POST.get("company")
        company = Company.objects.get(id=com_id)

        Support.objects.create(full_name=full_name,email=email,desc=desc,company=company)

        return redirect("/")