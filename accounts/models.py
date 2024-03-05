from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    USER_TYPE_CHOICES = (
        ('JOB_SEEKER','JOB_SEEKER'),
        ('COMPANY','COMPANY'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    full_name = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile_pic',null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    gender = models.CharField(max_length=10)
    resume = models.FileField(upload_to='resume',null=True,blank=True)
    user_type = models.CharField(max_length=25,default='JOB_SEEKER',choices=USER_TYPE_CHOICES)
    working_company_id = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.full_name)