from django.db import models
from jobs.models import Company

# Create your models here.
class Support(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    desc = models.TextField(null=True,blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self,request):
        return str(self.full_name)