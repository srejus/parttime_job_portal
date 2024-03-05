from django.db import models
from accounts.models import Account

from datetime import date


# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='company_user')
    company_name = models.CharField(max_length=100,null=True,blank=True)
    company_logo = models.ImageField(upload_to='company_logo')
    desc = models.CharField(max_length=200,null=True,blank=True)
    avg_rating = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.company_name)
    

class Employee(models.Model):
    employee = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='employee')
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee.full_name)
    


class Attendence(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def get_attendance_for_today(self):
        today = date.today()
        return self.objects.filter(created_at=today).exists()

    def get_attendance_for_current_month(self):
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = today
        return self.objects.filter(
            created_at__range=[start_of_month, end_of_month]
        )

    def __str__(self):
        return str(self.employee.employee.full_name)
    

class Review(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    review = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.user)+">"+str(self.company)