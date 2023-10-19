from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.contrib.auth import logout
from jobseeker.models import JobSeeker,AppliedJobs
from employer.models import Job,Employer,Questions
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.core import serializers
from xhtml2pdf import pisa
from io import BytesIO
import uuid
import json
import datetime
import random
def register_job_seeker(request):
    if request.method == 'POST':
        name = request.POST.get('jname')
        phone_number = request.POST.get('jphone')
        email = request.POST.get('jemail')
        password = request.POST.get('jpassword')
        normalized_email = email.lower()
        hashed_password  = make_password(password)

        email_exists = JobSeeker.objects.filter(email = normalized_email).exists()
        phone_exists = JobSeeker.objects.filter(phone = phone_number).exists()

        message = ''
        if email_exists:
            message = 'Email Already Exists'
        elif phone_exists:
            message = 'Phone Number is Taken'

        if email_exists or phone_exists:
            messages.error(request,message)
            return render(request,'forms/job_seeker.html')
        
        else:
            #name email password phone
            pk = uuid.uuid4()
            jobseeker = JobSeeker(id = pk,name=name,email=normalized_email,password=hashed_password,phone = phone_number)
            try:
                jobseeker.save()
                request.session['email'] = normalized_email
                return redirect('jobseeker-dashboard')
            except Exception as e:
                print(e)
                messages.error(request,"Internal Server Error. Please try again later.")
                return redirect('register_jobseeker')
            
    return render(request,'forms/job_seeker.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        normalized_email = email.lower()

        # print(normalized_email,password)

        message = ''
        if email == '':
            message = "Email address is required."
        
        elif password =='':
            message = "Password is required."

        if email =='' or password == '':
            messages.error(request,message)
            return redirect('login')

        else:
            jobseeker_exists = JobSeeker.objects.filter(email = normalized_email).exists()
            if jobseeker_exists:
                jobseeker = JobSeeker.objects.get(email = normalized_email)
                password_matched = check_password(password,jobseeker.password)
                if password_matched:
                    request.session['jobseeker_email'] = normalized_email
                    return redirect('jobseeker-dashboard')
                else:
                    messages.error(request,"Password doesn't matched.")
                    return redirect('login')
            else:
                messages.error(request,"Account with provided email doesn't exists.")
                return redirect('register_jobseeker')
    return render(request,'forms/login.html')


def jobseeker_dashboard(request):
    email = request.session.get('jobseeker_email',None)
    if email:
        job = Job.objects.order_by('job_id')
        paginator = Paginator(job,6)
        page_number = request.GET.get('page')
        pages = paginator.get_page(page_number)
        total_pages = paginator.num_pages #Returns total number of pages.

        return render(request,'jobseeker-dashboard/dashboard.html',{'job':job,'pages':pages,'lastpage':total_pages,'pagelist':[n+1 for n in range(total_pages)]})
    else:
        messages.error(request,"Session Expired. Please login here.")
        return redirect('login')

def statistics(request):
    email = request.session.get('jobseeker_email',None)
    if email:
        jobseeker = JobSeeker.objects.get(email = email)
        # check if jobseeker applied to any job or not.
        # may be 1 or more.
        message = ''
        applied_jobs = None
        has_applied = AppliedJobs.objects.filter(job_seeker = jobseeker).exists()
        if has_applied:
            applied_jobs = AppliedJobs.objects.filter(job_seeker = jobseeker)
            
        else:
            message = 'You havenot applied to any jobs yet.'
        
        context = {
            'message':message,
            'applied_jobs':applied_jobs
        }
        return render(request,'jobseeker-dashboard/components/statistics.html',context)
    else:
        messages.error(request,"Session Expired. Please Login here.")
        return redirect('login')
    
@xframe_options_exempt
def profile(request):
    email_add = request.session.get('jobseeker_email',None)
    if email_add:
        if request.method == 'POST':
            name = request.POST.get('name')
            # email = request.POST.get('email') Should not be changed randomly.
            address = request.POST.get('address')
            phone =  request.POST.get('phone')
            dob = request.POST.get('dob','')
            preference = request.POST.get('preference')
            qualification = request.POST.get('qualification')
            aboutyou = request.POST.get('aboutyou')
            cv = request.FILES.get('cv',None)
            experiences = request.POST.get('experiences')
            if dob == '':
                pass
            else:
                jobseeker.date_of_birth = dob

            jobseeker = JobSeeker.objects.get(email = email_add)
            if 'profile' in request.FILES:
                if jobseeker.profile:
                    default_storage.delete(jobseeker.profile.path)
                
                image  = request.FILES['profile']
                jobseeker.profile.save(image.name,image)
            
            if 'cv' in request.FILES:
                if jobseeker.cv:
                    default_storage.delete(jobseeker.cv.path)
                
                cv = request.FILES.get('cv')
                jobseeker.cv.save(cv.name,cv)
            
            jobseeker.name = name
            jobseeker.address = address
            jobseeker.phone = phone
            jobseeker.preferences = preference
            jobseeker.about_me = aboutyou
            jobseeker.qualification = qualification
            jobseeker.experiences = experiences           
            try:
                jobseeker.save()
            except Exception as e:
                print(e)

        jobseeker = JobSeeker.objects.get(email = email_add)
        return render(request,'jobseeker-dashboard/components/profile.html',{'data':jobseeker})
    else:
        messages.error(request,"Session Expired. Please login here.")
        return redirect('login')
    

def logout_jobseeker(request):
    logout(request)
    return redirect('home_page')


def browse_job(request,id):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:   
            allow = True
            job = Job.objects.get(job_id = id)
            jobseeker = JobSeeker.objects.get(email=email)
            is_applied = AppliedJobs.objects.filter(job__job_id = id,job_seeker__id = jobseeker.id).exists()
            message = ''
            # Prevent jobseeker from applying job after deadline
            if datetime.date.today() > job.deadline:
                allow = False
                message = "Application closed."                
            

            if is_applied:
                allow = False
                message = "You've already applied for this job."
                

            print(is_applied)
        except Exception as e:
            print("Exception in browse_job",e)
        context = {"data":job,"allowed":allow,"message":message,"isapplied":is_applied}
        return render(request,'jobseeker-dashboard/components/browsejobs.html',context)

    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('login')
    
def view_employer(request,employer):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:
            employer = Employer.objects.get(emp_id = employer)
        except Exception as e:
            pass
        return render(request,'jobseeker-dashboard/components/aboutemployer.html',{'employer':employer})
    else:
        messages.error(request,"Session Expired. Please Login again.")
        return redirect('login')

def download_cv(request,jobseeker_id):
    email = request.session.get('jobseeker_email',None)
    if email:
        try:
            # print("Entering try")
            jobseeker = JobSeeker.objects.get(id = jobseeker_id)

            context = {'data':jobseeker}
            template = get_template('jobseeker-dashboard/components/downloadcv.html')
            html = template.render(context)
            pdf_buffer = BytesIO()
            pisa.CreatePDF(html, dest=pdf_buffer)
            pdf_buffer.seek(0) #set buffer position to start.
            response = HttpResponse(pdf_buffer,content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{jobseeker.name}_CV.pdf"'
            return response
        except Exception as e:
            pass
    else:
        messages.error(request,"Please Sign in here.")
        return redirect('login')

def applyjob(request):
    email = request.session.get('jobseeker_email',None)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if email:
        if is_ajax:
            if request.method == 'POST':
                data = json.load(request)
                coverletter = data.get('coverletter')
                job_id = data.get('job_id')
                job = Job.objects.get(job_id = job_id)
                jobseeker = JobSeeker.objects.get(email = email)
                try:
                    pk = uuid.uuid4()
                    appliedjobs = AppliedJobs(id = pk, job = job,job_seeker = jobseeker,coverletter = coverletter)
                    appliedjobs.save()
                    response_data = {'success': 'Application received.'}
                    return HttpResponse(json.dumps(response_data),content_type = 'application/json',status=200)
                except Exception as e:
                    print("Exception in applyjob view",e)
    
    else:
        messages.error(request,"Please Sign in before you proceed")
        return redirect('login')

def quiz(request,id):
    email = request.session.get('jobseeker_email',None)
    if email:
        jobseeker = JobSeeker.objects.get(email = email)
        # print(jobseeker)
        #Check if jobseeker has applied for a job or not.
        is_job_applied = AppliedJobs.objects.filter(job_seeker = jobseeker).exists()
        questions = None
        message = ''
        if is_job_applied:
            job = AppliedJobs.objects.filter(job_seeker = jobseeker)
            get_job = Job.objects.get(job_id = id)
            questions_exists = Questions.objects.filter(job = get_job).exists()
            if questions_exists:
                questions = Questions.objects.filter(job = get_job)
                question_list = list(questions)
                random.shuffle(question_list)

            else:
                message = "No Questions are posted by employer."
        else:
            pass
        context = {
            'jobseeker':jobseeker,
            'questions':question_list,
            'message':message,
        }
        return render(request,"jobseeker-dashboard/quiz.html",context)
    else:
        messages.error(request,"session Expired.")
        return redirect('login')

def get_quizes(request,job_id,employer):
    email = request.session.get('jobseeker_email',None)
    question_set = []
    error_message = []
    if email:
        employer_exists = Employer.objects.filter(emp_id = employer).exists()
        if employer_exists:
            employer = Employer.objects.get(emp_id = employer)
            jobs = Job.objects.filter(employer = employer)
            #check if job has questions
            has_questions = Questions.objects.filter(job__job_id = job_id).exists()
            if has_questions:
                questions = Questions.objects.filter(job__job_id = job_id)
                for question in questions:
                    question_list = {
                        'id':question.question_id,
                        'question':question.question,
                        'correctAnswer':question.correct_answer,
                        'option_one':question.option_one,
                        'option_two':question.option_two,
                        'option_three':question.option_three,
                        'option_four':question.option_four,
                    }
                    question_set.append(question_list)
            else:
                error_message.append({"message":"No data found"})
        else:
            error_message.append({"message":"Employer not found"})




            
        response_data = {'questions':question_set}
        response_json = json.dumps(response_data)
        context = {
            'error_message':error_message,
            'questions':response_json
        }        
        return JsonResponse(context)
    else:
        messages.error(request,"session Expired.")
        return redirect('login')