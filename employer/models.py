from django.db import models

# Employer posts job has JobQuestions.
class Employer(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=50,null=False,blank=False,verbose_name='Employer name')
    emp_phone_number = models.CharField(max_length=11,null=False,blank=False,verbose_name='Employer number')
    emp_email = models.EmailField(verbose_name='Employer Email',null=False,blank=False,unique=True)
    emp_password = models.CharField(max_length=25,null=False,blank=False,verbose_name='Employer Password')
    about_employer = models.TextField(verbose_name='About Employer',blank=True,null=True)
    emp_profile = models.FileField(upload_to='employer-profile/',null=True,verbose_name='Profile Photo')
    # emp_address = models.TextField(verbose_name='Address',null=False,blank=False,default="Birtamode")
    def __str__(self):
        return self.emp_name
    

LOCATION_TYPE = (
    ('Hybrid',"Hybrid"),
    ('On Site',"On Site"),
    ('Online',"Online")
    )
JOB_TYPE = (
    ('Full time',"Full Time"),
    ('Part Time',"Part Time"),
    ('Freelance',"Freelance")
    )

class Job(models.Model):
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE)
    job_id = models.AutoField(primary_key=True)
    job_type = models.CharField(max_length=50,choices=JOB_TYPE,blank=False,null=False ,verbose_name='Job type')
    job_position = models.CharField(verbose_name="Position",max_length=100,null=False,blank=False)
    job_requirement = models.CharField(verbose_name="Requirements",max_length=100,null=False,blank=False)
    job_description = models.TextField(verbose_name="Description",null=False,blank=False)
    salary = models.TextField(max_length=30,blank=True,null=True);
    location_type = models.TextField(choices=LOCATION_TYPE,blank=False)


    def __str__(self):
        return self.job_type
    

class Questions(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name = 'question')
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(verbose_name="Questions",max_length=150,blank=False,null=False)
    marks = models.CharField(max_length=50,null=False,blank=False,default=5)

    class Meta:
        verbose_name_plural = 'Questions'

    def __str__(self) -> str:
        return self.question

class Answers(models.Model):
    question = models.ForeignKey(Questions, related_name='question_answer',on_delete=models.CASCADE)
    answer = models.CharField(max_length=100,null=False,blank=False)
    is_answer_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.answer

