from django.shortcuts import render

# Create your views here.


def register_job_seeker(request):
    return render(request,'forms/job_seeker.html')

def login(request):
    return render(request,'forms/login.html')



def jobseeker_dashboard(request):
    return render(request,'jobseeker-dashboard/dashboard.html')