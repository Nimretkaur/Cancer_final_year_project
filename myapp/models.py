from django.db import models
from datetime import date
from datetime import datetime

# Create your models here.
# class person(models.Model):
#     first_name = models.CharField(max_length = 30)
#     last_name = models.CharField(max_length = 30)
#     def __str__(self):
#         return self.first_name

class myreview(models.Model):
    rev_sub = models.CharField(max_length = 30)
    rev_msg = models.TextField()
    user_email = models.EmailField()
    def __str__(self):
        return self.rev_sub

class myhelp(models.Model):
    help_sub = models.CharField(max_length = 30)
    help_msg = models.TextField()
    user_email = models.EmailField()
    def __str__(self):
        return self.help_sub

class mycontactus(models.Model):
    cs_name = models.CharField(max_length = 30)
    cs_email = models.EmailField()
    cs_address = models.TextField(null=True,blank=True)
    cs_phone = models.IntegerField(null=True,blank=True)
    cs_msg = models.TextField()
    def __str__(self):
        return self.cs_name

class myregister(models.Model):
    reg_name = models.CharField(max_length = 30)
    reg_email = models.EmailField()
    reg_phone = models.CharField(max_length = 12)
    reg_pass = models.CharField(max_length = 40)
    reg_cpass = models.CharField(max_length = 40)
    reg_bloodgroup = models.CharField(max_length = 10, null=True , blank=True)
    reg_city = models.CharField(max_length = 15, null=True , blank=True )
    reg_address = models.TextField(max_length = 1000, null=True , blank=True)
    reg_dob = models.DateField(max_length = 8, null=True , blank=True)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True , blank=True)
   
    def __str__(self):
        return self.reg_email


class mypatient(models.Model):

    patient_id = models.CharField(max_length=30)
    pat_img = models.ImageField(null=True,blank=True)
    pat_name = models.CharField(max_length = 30)
    pat_email = models.EmailField()
    pat_pass = models.CharField(max_length = 40)
    pat_contact = models.CharField(max_length = 12,null = True)
    pat_pincode = models.IntegerField(null = True)
    pat_address = models.CharField(max_length = 100,null = True)
    pat_city = models.CharField(max_length = 20,null = True)
    pat_state = models.CharField(max_length = 20,null = True)
    pat_dob = models.DateField(max_length = 8,null = True)
    pat_bloodgroup = models.CharField(max_length = 3,null = True)
    pat_age = models.IntegerField(null = True)
    #disease_id = models.ForeignKey(mydisease, on_delete = models.CASCADE)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    pat_gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null = True)

    def __str__(self):
        return self.patient_id


    def generate_age(self):
        pass


    def generate_patient_id(self):
        self.patient_id = self.pat_name[0:2]+"100"+str(self.id)


class myhospital(models.Model):
    # hospital_id = models.CharField(max_length=80)
    hosp_name = models.CharField(max_length = 80)
    hosp_img = models.ImageField(null=True,blank=True)
    hosp_contact = models.IntegerField(null=True , blank=True)
    hosp_pincode = models.IntegerField()
    hosp_city = models.CharField(max_length = 30)
    hosp_state = models.CharField(max_length = 30)
    hosp_fulladdress = models.CharField(max_length = 400)

    def __str__(self):
        return "10"+str(self.id)+"_"+self.hosp_name

    # def generate_hospital_id(self):
    #     self.hospital_id = "10"+str(self.id)+"_"+self.hosp_name


class myclinic(models.Model):
    # clinic_id = models.CharField(max_length=80)
    clin_name = models.CharField(max_length = 50)
    clin_img = models.ImageField(null=True,blank=True)
    clin_contact = models.IntegerField(null=True , blank=True)
    clin_pincode = models.IntegerField()
    clin_city = models.CharField(max_length = 30)
    clin_state = models.CharField(max_length = 30)
    clin_fulladdress = models.CharField(max_length = 400)
    clin_start_time = models.TimeField()
    clin_closing_time = models.TimeField()

    def __str__(self):
        return "10"+str(self.id)+"_"+self.clin_name

    # def generate_clinic_id(self):
    #     self.clinic_id = "10"+str(self.id)+"_"+self.clin_name

class mydiagnostic(models.Model):
    # diag_id = models.CharField(max_length=80)
    diag_name = models.CharField(max_length = 50)
    diag_img = models.ImageField(null=True,blank=True)
    diag_contact = models.IntegerField(null=True , blank=True)
    diag_pincode = models.IntegerField()
    diag_city = models.CharField(max_length = 30)
    diag_state = models.CharField(max_length = 30)
    diag_fulladdress = models.CharField(max_length = 400)
    diag_start_time = models.TimeField()
    diag_closing_time = models.TimeField()

    def __str__(self):
        return "10"+str(self.id)+"_"+self.diag_name

class mydoctor(models.Model):
    # doctor_id = models.CharField(max_length=20)
    doc_name = models.CharField(max_length = 30)
    doc_email = models.EmailField(null=True , blank=True)
    doc_contact = models.CharField(max_length = 12, null= True)
    doc_img = models.ImageField(null=True,blank=True)
    doc_experience = models.IntegerField()
    doc_pincode = models.IntegerField()
    doc_city = models.CharField(max_length = 20)
    doc_state = models.CharField(max_length = 20)
    qualification = models.TextField(null=True , blank=True)
    specialization = models.CharField(max_length = 80)
    doc_pass = models.CharField(max_length = 50)
    doc_img = models.ImageField(null=True,blank=True)
    clinic_id = models.ForeignKey(myclinic, on_delete = models.CASCADE,null=True,blank=True)
    hospital_id = models.ForeignKey(myhospital, on_delete = models.CASCADE,null=True,blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    doc_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return "100"+str(self.id)+"-"+self.doc_name

    # def generate_doctor_id(self):
    #     self.doctor_id = "100"+str(self.id)


class mydisease(models.Model):
    dise_name = models.CharField(max_length = 30)
    dise_description = models.CharField(max_length = 1000,null=True,blank=True)
    dise_url = models.URLField(null=True)



class myappointment(models.Model):
    patient_id = models.ForeignKey(mypatient, on_delete = models.CASCADE)
    doctor_id = models.ForeignKey(mydoctor, on_delete=models.CASCADE)
    app_time = models.TimeField(null=True,blank=True)
    app_applyTime_Date = models.DateTimeField()
    app_date = models.DateField()
    app_timeofday = models.CharField(max_length = 20)
    app_reason = models.TextField(null=True, blank = True)
    app_isactive = models.BooleanField(default=False)
    app_notes = models.TextField(null=True,blank=True)

    Appointment_Status = (
        ('A', 'Approved'),
        ('NA', 'Not Approved'),
        ('P', 'Pending')
    )

    app_status = models.CharField(max_length=2, choices=Appointment_Status,default='P')

    def __str__(self):
        return self.patient_id.pat_email+"--->"+self.doctor_id.doc_email

class mymessages(models.Model):
    mess_from = models.IntegerField()
    mess_to = models.IntegerField()
    mess_date = models.DateField()
    mess_time = models.TimeField()
    mess_message = models.TextField(max_length = 1000, null=True , blank=True)
    mess_attachment = models.FileField(null=True , blank=True)
    app_id = models.ForeignKey(myappointment, on_delete=models.SET_NULL, null=True)
