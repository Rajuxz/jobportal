from django.shortcuts import render
# from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'index.html')


def admin(request):
    return render(request,'admin-dashboard/adminlogin.html')

def admin_test(request):
    return render(request,'admin-dashboard/dashboard.html')



def admin_home(request):
    return render(request,'admin-dashboard/adminhome.html')