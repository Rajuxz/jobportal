from django.urls import path
from .views import *
urlpatterns = [
    path('',jobseeker_dashboard,name="jobseeker-dashboard"),
    path('register-job-seeker/',register_job_seeker,name='register_jobseeker'),
    path('login/',login,name="login"),
    path('jobseeker-dashboard',jobseeker_dashboard,name='jobseeker-dashboard'),
    path('create-profile',create_profile,name="create-profile"),
    path('profile',profile,name="profile"),  
]
