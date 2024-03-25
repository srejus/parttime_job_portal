from django.db import models

from hr.models import Company
from accounts.models import Account

# Create your models here.


class JobListing(models.Model):
    PAY_CHOCIES = (
       ( 'DAILY','DAILY'),
       ('HOURLY','HOURLY'),
       ('WEEKLY','WEEKLY'),
       ('MONTHLY','MONTHLY'),
    )
    SHIFT_CHOICES = (
        ('DAY','DAY'),
        ('EVENING','EVENING'),
        ('NIGHT','NIGHT'),
    )
    posted_by_company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='job_posted_by')
    title = models.CharField(max_length=100,null=True,blank=True)
    desc = models.CharField(max_length=200,null=True,blank=True)
    salary_from = models.FloatField(null=True,blank=True)
    salary_to = models.FloatField(null=True,blank=True)
    daily_salary = models.FloatField(default=0.0)
    pay_type = models.CharField(max_length=50,default='DAILY',choices=PAY_CHOCIES)
    location = models.CharField(max_length=100,null=True,blank=True)
    shift_type = models.CharField(max_length=100,null=True,blank=True,choices=SHIFT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('RECEIVED','RECEIVED'),
        ('ACCEPTED','ACCEPTED'),
        ('REJECTED','REJECTED'),
    )
    applied_by = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='applied_by')
    job = models.ForeignKey(JobListing,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default='RECEIVED',choices=STATUS_CHOICES)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.applied_by) +" - "+ str(self.job)