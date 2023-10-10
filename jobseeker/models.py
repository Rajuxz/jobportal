from django.db import models
from employer.models import Job
import datetime
import os

def filepath(request,filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename  = "%s%s" % (time_now,old_filename)
    return os.path.join('jobseeker-cv/',filename)

class JobSeeker(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50,null=False,blank=False,verbose_name='Jobseeker Name')
    email = models.EmailField(null=False, blank=False, unique=True,verbose_name='Jobseeker Email')
    password = models.TextField(max_length=255,blank=False,null=False,verbose_name='Jobseeker Password')
    phone = models.TextField(max_length=15,blank=False,null=False,verbose_name='Jobseeker Phone')
    date_of_birth = models.DateField(null=True, blank=True)
    about_me = models.TextField(null=True,blank=True,verbose_name='About You')
    qualification = models.TextField(blank=True,null=True,verbose_name="Qualifications")
    preferences = models.TextField(null=True,blank=True,verbose_name="Job Preferences")
    cv = models.FileField(upload_to=filepath,verbose_name='CV')


    def __str__(self):
        return self.name
    
class AppliedJobs(models.Model):
    id = models.UUIDField(primary_key=True)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker,on_delete=models.CASCADE)

