from django.shortcuts import render
from myapp.models import myreview
from myapp.models import myhelp
from myapp.models import mypatient
from myapp.models import mycontactus
from myapp.models import mydoctor
from django.shortcuts import redirect
from datetime import datetime
from datetime import date
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from myapp.models import mydiagnostic
from myapp.models import myhospital
from myapp.models import myclinic
from myapp.models import myappointment
from myapp.models import mymessages, mydisease
from django.core import serializers
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random as rn
from Cancer import settings
from matplotlib import pylab
from pylab import *
from PIL import Image, ImageDraw
import PIL, PIL.Image
from io import StringIO
#warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
#import statsmodels.api as sm
import matplotlib
from io import BytesIO
import io
import base64
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from django.core.mail import send_mail
# for api for latest news for index Page
from newsapi import NewsApiClient
from random import choices


# Create your views here.
def test(request):
    us = User.objects.all()

    for u  in us:
        print(u.username)

    return HttpResponse("<h1>Done</h1>")    

def form(request):
    return render(request,'form.html',{})

# ,\"Cervical Cancer\",\"Prostate Cancer\", \"living Healthy\" 

def get_news():
    newsapi = NewsApiClient(api_key='c163ff886deb44159a600cc569dd2109')
    all_articles = newsapi.get_everything(q='\"Prostate Cancer\",\"Lung Cancer\",\"Breast Cancer\" ',               
                                      language='en',
                                      sort_by='relevancy',
                                      )

    print(all_articles.get('status'))
    articles = choices(all_articles['articles'], k=3)

    return articles

def index(request):
    articles = get_news()
    # print(articles)
    return render(request,'index.html',{'articles': articles})

def register(request):
    if request.method == 'POST':
        name = request.POST.get('fn')
        email = request.POST.get('em')
        phone = request.POST.get('phn')
        opass = request.POST.get('npwd') 
        cpass = request.POST.get('cpwd')
        user_em = mypatient.objects.filter(pat_email = email)

        if len(user_em) > 0:
            temp = 'Already registered. Please Login'
            return render(request, 'register.html', {'temp':temp})
        else:
            if opass == cpass:
                post = mypatient()
                post.pat_name = name
                post.pat_email = email
                post.pat_contact = phone
                post.pat_pass = opass
                post.save()

                post.generate_patient_id()
                post.save()
                temp = 'Registered, Please login'
                return render(request,'register.html',{'temp':temp})
            else:
                temp = 'New password and Confirm password does not match'
                return render(request, 'register.html',{'temp':temp})

    return render(request,'register.html',{})

def contactus(request):
    if request.method == "POST":
        post = mycontactus()
        post.cs_name = request.POST.get('fn')
        post.cs_email = request.POST.get('em')
        post.cs_address = request.POST.get('add')
        post.cs_phone = request.POST.get('phn')
        post.cs_msg = request.POST.get('message')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'contactus.html',{'res':res})
    else:
        return render(request,'contactus.html',{})

def login(request):
    if request.method == "POST":   # if user submit the data
        formpost = True
        useremail = request.POST.get('em')  #getting data from the form, email and password
        pw = request.POST.get('npwd')
        errormessage = ""
        expert = mypatient.objects.filter(pat_email = useremail, pat_pass = pw) 
        #filter operation will filter from mypatients model and will return a list.

        k = len(expert) # list can be empty if or have items 
        if k>0:         # if len of list is greater than zero means, user has registered before.
            print("Valid Credentials")
            request.session['em'] = useremail
            request.session['user_id'] = expert[0].id
            request.session['pat_name'] = expert[0].pat_name
            
            return redirect('/dashboard')

        else:           # if len of list is zero means, user has not registered or is putting invalid credentials.
            res = 1
            print("Invalid Credentials")
            errormessage = "Invalid Credentials"
            return render(request,'login.html',{'formpost':formpost,'res':res})  # returning a msg for the user for Invalid Credentials
    
    else:
        formpost = False
        return render(request,'login.html',{'formpost':formpost})

def recoverpassword(request):

    if request.method == 'POST':
        em = request.POST.get('em')
        res = None
        if mypatient.objects.filter(pat_email = em).exists():
            user = mypatient.objects.get(pat_email = em)

            subject = 'Password'
            
            html_message= """<h3>Hello</h3>"""+user.pat_name+""" Your password is
                            <b> """+user.pat_pass+"""</b> <a href='http://localhost:8000/login/'> Click Here to Login </a>"""
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [user.pat_email, ]
            try: 
                send_mail(subject, email_from , recepient_list , html_message = html_message)
                res = "Your Password is sent successfully to your mail"
            except Exception as E:
                print(E)    
            return render(request, 'recoverpassword.html', {'res':res})


        else:
            res = 'User does not exist'
           
            return render(request, 'recoverpassword.html', {'res':res})
    
    return render(request, 'recoverpassword.html', {'res':''})

def footer(request):
    return render(request,'footer.html',{})

def help(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    if request.method == "POST":
        post = myhelp()
        post.help_sub = request.POST.get('sub')
        post.help_msg = request.POST.get('msg')
        post.user_email = request.session.get('em')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'help.html',{'res':res})
    else:
        return render(request,'help.html',{})

def dochelp(request):
    if not request.session.has_key('docem'):
        return redirect('/login')
    if request.method == "POST":
        post = myhelp()
        post.help_sub = request.POST.get('sub')
        post.help_msg = request.POST.get('msg')
        post.user_email = request.session.get('docem')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'doctorF/dochelp.html',{'res':res})
    else:
        return render(request,'doctorF/dochelp.html',{})

def editprofile(request):

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    if not request.session.has_key('em'):
        return redirect('/login')
    userdetail = mypatient.objects.get(pat_email = request.session['em'])
    if request.method == 'POST':
        type_form = request.POST.get('type')
        if type_form == "1":
            userdetail.pat_img = request.FILES.get('image')
            userdetail.save()
        else:
            detail = mypatient.objects.get(pat_email = request.session['em'])
            detail.pat_name = request.POST.get('fn')
            detail.pat_contact = request.POST.get('phn')
            detail.pat_dob = request.POST.get('dob')
            detail.pat_bloodgroup = request.POST.get('bg')
            detail.pat_pincode = request.POST.get('pin')
            detail.pat_city = request.POST.get('city')
            detail.pat_state = request.POST.get('state')
            detail.pat_address = request.POST.get('address')
            detail.pat_gender = request.POST.get('gen')

            detail.save()
            
            data = mypatient.objects.get(pat_email = request.session['em'])
            print('age is ',calculate_age(data.pat_dob))
            data.pat_age = int(calculate_age(data.pat_dob))
            data.save()
            return render(request,'dashboard.html',{'us':data})

    print(userdetail.id)
    patient_dob = None

    if userdetail.pat_dob!=None:
        patient_dob = userdetail.pat_dob.strftime("%Y-%m-%d")


    return render(request,'editprofile.html',{'us':userdetail, 'pat_dob':patient_dob})

def changepassword(request):
    if not request.session.has_key('em'):
       return redirect('/login')
    if request.method == 'POST':
        temp = mypatient.objects.get(pat_email = request.session['em'])
        password = request.POST.get('old')
        newpwd = request.POST.get('npwd')
        confirmpwd = request.POST.get('cpwd')
        
        if(newpwd == confirmpwd):
            p =temp.pat_pass
            #print("db password",p)
            if(password == p):
                temp.pat_pass = newpwd
                temp.save()
                rest = "Password Changed"
                print("Password Updated")
                return render(request,'Changepassword.html',{'rest':rest})
            else:
                print("Password not updated")
                res = "Invalid Current Password"
                return render(request,'changepassword.html',{'res':res})
        else:
            res = "Confirm password and new password don't match"
            return render(request,'changepassword.html',{'res':res})
    else:
        return render(request,'changepassword.html')

def review(request):                     
    if not request.session.has_key('em'):  
        return redirect('/login')          
    if request.method == "POST":           
        post = myreview()                        
        post.rev_sub = request.POST.get('name')   
        post.rev_msg = request.POST.get('msg')    
        post.user_email = request.session.get('em')

        try:
            post.save()
            res = 1
        except Exception:
            res = 2

        return render(request, 'review.html', {'res':res})
    else:
        return render(request,'review.html',{})

def base(request):
    return render(request,'base.html',{})

def sidebar(request):
    return render(request,'sidebar.html',{})

def logout(request):
    if not request.session.has_key('em'):
        return redirect("/login")
    del request.session['em']
    return redirect('/login')

def profile(request):
    if not request.session.has_key('em'):
        return redirect('/login')
    userdetail = mypatient.objects.get(pat_email= request.session['em'])
    return render(request,'profile.html',{'user':userdetail})

def dashboard(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    cur_user = mypatient.objects.get(pat_email = request.session.get('em'))

    count_approved_app = myappointment.objects.filter(patient_id = cur_user,app_status='A',app_isactive = True).count()

    count_pending_app = myappointment.objects.filter(patient_id = cur_user, app_status = 'P' , app_date__gte = date.today()).count()

    count_active_chat = myappointment.objects.filter(patient_id = cur_user, app_status = 'A' , app_isactive=True ).count()

    return render(request,'dashboard.html',{'count_active':count_approved_app, 'count_pending': count_pending_app, 'count_active_chat':count_active_chat})

def chatwithdoctor(request):
    if not request.session.has_key('em'):
        return redirect("/login") 
    
    curr_pat = mypatient.objects.get(pat_email = request.session.get('em'))

    appointments = myappointment.objects.filter(patient_id = curr_pat, app_isactive = True)
    selected_field = 'enabled'

    if request.method == 'POST':
        selected_field = request.POST.get('apply_filter')

        if selected_field == 'enabled':
            appointments = myappointment.objects.filter(patient_id = curr_pat, app_isactive = True, app_status = 'A')
            
        elif selected_field == 'disabled':
            appointments = myappointment.objects.filter(patient_id = curr_pat, app_isactive = False, app_status = 'A')  # otheriwise it will show pending and not approved patients also

    print(appointments,selected_field)
    return render(request,'chatwithdoctor.html',{'selected_field':selected_field,'appointments':appointments})


def chatpage(request, id):
    if not  request.session.has_key('em'):
        return redirect('/login')

    current_user = mypatient.objects.get(pat_email = request.session.get('em'))
    
    appointment = myappointment.objects.get(id = id)

    messages = mymessages.objects.filter(app_id = appointment)

    # print(latest_user_appointed_doc_messages)

    return render(request,'chatpage.html',{'messages':messages, 'appointment':appointment })

def getmessages(request):
    app_id = request.GET.get('app_id')

    user_appointment = myappointment.objects.get(id = int(app_id))
    messages = mymessages.objects.filter(app_id = user_appointment.id)
    ser_messages = serializers.serialize('json', messages)
    
    return JsonResponse({'messages':ser_messages}, safe=False)


def user_chat_update(request):
    if request.method == 'POST':
        message_text = request.POST.get('msg')
        attachment  = request.FILES.get('attachment')
        appointment_id = request.POST.get('app_id')
        doctor_id = request.POST.get('doc_id')

        today_time_date = datetime.datetime.now()

        message  =  mymessages()
        message.mess_from = mypatient.objects.get(pat_email = request.session.get('em')).id
        
        message.mess_to =   doctor_id

        message.mess_date = today_time_date.date()
        message.mess_time = today_time_date.time()

        message.mess_message = message_text
        if attachment:
            message.mess_attachment = attachment

        message.app_id = myappointment.objects.get(id = int(appointment_id))

        message.save()

        ser_message = serializers.serialize('json', [message,])

        print(message, attachment, appointment_id, doctor_id)
        return JsonResponse({'message': ser_message}, safe=False)


def doctorspage(request):
    if not request.session.has_key('em'):
        return redirect('/login')
    docdata = mydoctor.objects.all()
    return render(request,'doctorspage.html',{'doctors':docdata})

def labs(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    labdata = mydiagnostic.objects.all()
    return render(request,'labs.html',{'labs':labdata})

def hospitals(request):
    if not request.session.has_key('em'):
        return redirect('/login')
        # city = mypatients.objects.get(email = request.session.get('em')).city
        # docs =  doc.objects.filter(city = city)
    hospitaldata = myhospital.objects.all()
    return render(request,'hospitals.html',{'hospitals':hospitaldata})

def clinics(request):
    if not request.session.has_key('em'):
        return redirect('/login')

    clinicdata = myclinic.objects.all()
    return render(request,'clinics.html',{'clinics':clinicdata})

def userappointment(request, id):
    
    if request.method =='POST':
        ap = myappointment()
        ap.patient_id = mypatient.objects.get(pat_email = request.session.get('em'))
        ap.doctor_id = mydoctor.objects.get(id= id)
        userapp_date = request.POST.get('dateforapp')
        userapp_dayoftime = request.POST.get('tofd')
        userapp_notes = request.POST.get('notes')
        ap.app_applyTime_Date = datetime.datetime.now()
        ap.app_timeofday = userapp_dayoftime
        ap.app_notes = userapp_notes
        ap.app_date = userapp_date
        # print(userapp_date,userapp_dayoftime,userapp_nates)
        ap.save()
       
    us = mypatient.objects.get(pat_email = request.session.get('em'))
    return render(request,'appointmentpage.html',{'user':us})

# Doctor Panel Pages
def docsidebar(request):
    # doctorName = mydoctor.objects.get(doc_name= request.session['name'])
    doctordetail = mydoctor.objects.get(doc_email= request.session['docem'])
    print(doctordetail)
    return render(request,'doctorF/docsidebar.html',{'doctor': doctordetail})

def docdashboard(request):
    if not request.session.has_key('docem'):
        return redirect('/doclogin')
    
    cur_doc = mydoctor.objects.get(doc_email = request.session.get('docem'))

    count_active_patients = myappointment.objects.filter(doctor_id = cur_doc,app_status='A',app_isactive = True).count()

    count_pending_appointments = myappointment.objects.filter(doctor_id = cur_doc , app_status = 'P' , app_date__gte = date.today()).count()

    return render(request,'doctorF/docdashboard.html',{'count_active':count_active_patients, 'count_pending': count_pending_appointments})

def docprofile(request):
    if not request.session.has_key('docem'):
        return redirect('/doclogin')
    docdetail = mydoctor.objects.get(doc_email= request.session['docem'])
    return render(request,'doctorF/docprofile.html',{'doctor': docdetail})

def doceditprofile(request):
    if not request.session.has_key('docem'):
        return redirect('/doclogin')
    docdetail = mydoctor.objects.get(doc_email = request.session['docem'])
    if request.method == 'POST':
        type_form = request.POST.get('type')
        if type_form == "1":
            docdetail.pat_img = request.FILES.get('image')
            docdetail.save()
        else:
            detail = mydoctor.objects.get(doc_email = request.session['docem'])
            detail.doc_name = request.POST.get('fn')
            detail.doc_contact = request.POST.get('phn')
            detail.doc_gender = request.POST.get('gen')
            detail.doc_experience = request.POST.get('exp')
            detail.doc_pincode = request.POST.get('pin')
            detail.doc_city = request.POST.get('city')
            detail.doc_state = request.POST.get('state')
            detail.qualification = request.POST.get('quali')
            detail.specialization = request.POST.get('specia')
            detail.save()
            data = mydoctor.objects.get(doc_email = request.session['docem'])
            return render(request,'doctorF/docdashboard.html',{'us':data})

    return render(request,'doctorF/doceditprofile.html',{'us':docdetail})

def doclogin(request):
    if request.method == "POST":
        formpost = True
        doctoremail = request.POST.get('docem')
        pw = request.POST.get('npwd')
        errormessage = ""
        expert = mydoctor.objects.filter(doc_email = doctoremail, doc_pass = pw)
        if len(expert)>0:
            print("Valid Credentials")
            request.session['docem'] = doctoremail
            request.session['doc_name'] = expert[0].doc_name
            request.session['doc_id'] = expert[0].id
            # return render(request,'doctorF/docdashboard.html',{})
            return redirect('docdashboard')
        else:
            res = 1
            print("Invalid Credentials")
            errormessage = "Invalid Credentials"
            return render(request,'doctorF/doclogin.html',{'res':res})
    
    else:
        formpost = False
        return render(request,'doctorF/doclogin.html',{})

def doclogout(request):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")
    del request.session['docem']
    del request.session['doc_name']
    return redirect('doclogin')

def docappointment(request):
    doc = mydoctor.objects.get(doc_email = request.session['docem'])

    if request.method == 'POST':
        type_of_form = request.POST.get('type') # we have 3 forms, getting which form is submit

        if type_of_form  == "1":    #for accept button, doctor needs to submit the timings for the appointment
            app_id = request.POST.get('app_id')
            appointment = myappointment.objects.get(id = int(app_id))

            appointment.app_time = request.POST.get('timing') #getting timing from the form
            appointment.app_reason = None                     # filling other values in myappointment model
            appointment.app_status = 'A'
            appointment.app_isactive = True
            appointment.save()

        elif type_of_form == "2":    #for cancel button, doctor need to submit the reason.
            app_id = request.POST.get('app_id')
            print(app_id)
            appointment = myappointment.objects.get(id = int(app_id))

            appointment.app_time = None
            appointment.app_reason = request.POST.get('reason')
            appointment.app_status = 'NA'
            appointment.save()

        elif type_of_form == "3":    # for choosing which appointments, doctor wants to see.
            app_filter = request.POST.get('filter')
            filter_date = request.POST.get('date')
            print(app_filter,filter_date)
            # applying if elif conditions to show particular appointments only 
            if app_filter == 'pending_appointments':
                appointments = myappointment.objects.filter(app_status='P', app_date = filter_date, doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})

            elif app_filter == 'approved_appointments':
                appointments = myappointment.objects.filter(app_status='A', app_date = filter_date,doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})
            elif app_filter == 'all_appointments':
                appointments = myappointment.objects.filter(app_date = filter_date,doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})    

            elif app_filter == 'rejected_appointments':
                appointments = myappointment.objects.filter(app_status='NA', app_date = filter_date,doctor_id = doc)
                return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'selected_field': app_filter, 'entered_date': filter_date})    

  
    # will show all apointments of today
    appointments = myappointment.objects.filter(doctor_id = doc, app_status = 'P')
    return render(request,'doctorF/docappointment.html',{'appointments':appointments, 'entered_date': date.today().strftime('%Y-%m-%d')} )

def userappointmentstatus(request):
    user = mypatient.objects.get(pat_email = request.session['em'])
    selected_field = 'all_appointments'
    if request.method == 'POST':
        type_of_form = request.POST.get('type')

        app_filter = request.POST.get('filter')
        print(app_filter)

        if app_filter == 'pending_appointments':
            userappointments = myappointment.objects.filter(app_status='P', patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})

        elif app_filter == 'approved_appointments':
            userappointments = myappointment.objects.filter(app_status='A',  patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})
        elif app_filter == 'all_appointments':
            userappointments = myappointment.objects.filter( patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})    

        elif app_filter == 'rejected_appointments':
            userappointments = myappointment.objects.filter(app_status='NA', patient_id = user )
            return render(request,'userappointmentstatus.html',{'userappointments':userappointments, 'selected_field': app_filter})    

  
    # will show all apointments of today
    appointments = myappointment.objects.filter(patient_id = user)
    return render(request,'userappointmentstatus.html',{'userappointments':appointments,'selected_field':selected_field} )

def docchangepassword(request):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")
    if request.method == 'POST':
        temp = mydoctor.objects.get(doc_email = request.session['docem'])
        password = request.POST.get('old')
        newpwd = request.POST.get('npwd')
        confirmpwd = request.POST.get('cpwd')
        
        if(newpwd == confirmpwd):
            p =temp.doc_pass
            if(password == p):
                temp.doc_pass = newpwd
                temp.save()
                rest = "Password Changed"
                print("Password Updated")
                return render(request,'doctorF/docchangepassword.html',{'rest':rest})
            else:
                print("Password not updated")
                res = "Invalid Current Password"
                return render(request,'doctorF/docchangepassword.html',{'res':res})
        else:
            res = "Confirm password and new password don't match"
            return render(request,'doctorF/docchangepassword.html',{'res':res})
    else:
        return render(request,'doctorF/docchangepassword.html',{})

def docpatients(request):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")  

    curr_doc = mydoctor.objects.get(doc_email = request.session.get('docem'))

    appointments = myappointment.objects.filter(doctor_id = curr_doc, app_isactive = True)
    selected_field = 'enabled'

    if request.method == 'POST':
        selected_field = request.POST.get('apply_filter')

        if selected_field == 'enabled':
            appointments = myappointment.objects.filter(doctor_id = curr_doc, app_isactive = True, app_status = 'A')
            
        elif selected_field == 'disabled':
            appointments = myappointment.objects.filter(doctor_id = curr_doc, app_isactive = False, app_status = 'A')  # otheriwise it will show pending and not approved patients also

    data = []
    for app in appointments:
        # check whether we have added disease detail for that appointment and if yes then add in a 
        # # tuple and then append it into list otherwise append none on place 
        if mydisease.objects.filter(appointment_id = app).exists():
            disease_associated = mydisease.objects.get(appointment_id = app.id)
            data.append( (app, disease_associated) ) 

        else:
            data.append( (app, None) ) 

    return render(request,'doctorF/docpatients.html',{'appointments_data':data,'selected_field':selected_field})


def enable_disable(request):
    app_id = request.GET.get('app_id')
    status = request.GET.get('status')

    print(app_id, status)
    appointment = myappointment.objects.get(id = app_id)

    if status == "enable":
        appointment.app_isactive = True
    elif status == "disable":
        appointment.app_isactive = False

    appointment.save()

    print(app_id , status)
    return JsonResponse({'res': True})

def docchatpage(request, appid=None):
    if not request.session.has_key('docem'):
        return redirect("/doclogin")

    if request.method == 'POST':
        type_of_form = request.POST.get('type')
        print(type_of_form)
        if type_of_form == "1":
            disease_name = request.POST.get("dis")
            disease_notes = request.POST.get("notes")
            app_id = request.POST.get('app_id')
            print(disease_name, disease_notes)

            if mydisease.objects.filter(appointment_id = app_id).exists():
                dis = mydisease.objects.get(appointment_id = app_id)
                dis.dise_name = disease_name
                dis.dise_description = disease_notes
                dis.save()
            else:  
                disease = mydisease()
                disease.dise_name = disease_name
                disease.dise_description = disease_notes
                disease.appointment_id = myappointment.objects.get(id = app_id)

                disease.save()

            appid = app_id

        elif type_of_form == "2":
            message_text = request.POST.get('msg')
            attachment = request.FILES.get('attachment')
            appointment_id = request.POST.get('app_id')
            patient_id = request.POST.get("pat_id")

            today_time_date = datetime.datetime.now()

            message = mymessages()
            message.mess_from = mydoctor.objects.get(doc_email = request.session.get('docem')).id
            message.mess_to = patient_id
            message.mess_date = today_time_date.date()
            message.mess_time = today_time_date.time()
            message.mess_message = message_text
            if attachment:
                message.mess_attachment = attachment
            
            message.app_id = myappointment.objects.get(id = int(appointment_id))   
            message.save()
            ser_message = serializers.serialize('json',[message,])
            
            return JsonResponse( {'message':ser_message}, safe=False )
    

    appointment = myappointment.objects.get(id = appid)
    all_messages = mymessages.objects.filter(app_id = appointment)

    disease_detail = None
    try:
        disease_detail = mydisease.objects.get(appointment_id = appointment)
    except Exception as e:
        print('No data')

    return render(request,'doctorF/docchatpage.html',{'all_messages':all_messages, 'appointment':appointment, 'disease_detail':disease_detail})



## Visualizations 
# Visualization Lung Survival Rates
def visLungSurvival(request):
    return render(request,'visLungSurvival.html',{}) 

def visLSTopCY(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 10), dpi=95,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        matplotlib.rcParams['axes.titlepad'] = 0   #The offset of the title from the top of the axes, in points. Default is None
        # matplotlib.rcParams['axes.autolimit_mode'] = 'round_numbers'
        # visualization code

        df = pd.read_csv('five-year-survival-rates-from-lung-cancer.csv')
        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]
        n = int(request.POST.get('topc'))

        df1 = df1.sort_values('Lung',ascending = False)
        df1 = df1.iloc[:n,:]
        
        plt.grid()
        ax = sns.barplot(x = 'Lung', y = 'Entity',data=df1)
        for index, value in enumerate(df1['Lung']):
            plt.text(value+0.4, index+0.1, int(value),color='black',fontsize=11)
        ax.set_ylabel("Countries",fontsize=18)
        ax.set_xlabel("Counts",fontsize=18)
        
        plt.title("Survival Lung Cancer Rates in Top "+str(n) +" Countries",loc='left')
        plt.tight_layout()   
        # plt.ylim(-1,16)
        # plt.xlim(0,40) 
        plt.ylim(0,n)      
          
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png',bbox_inches='tight')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visLSTopCY.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visLSTopCY.html',{})

def visLSYear(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(13,7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        # matplotlib.rcParams['axes.titlepad'] = 0
        # matplotlib.rcParams['axes.autolimit_mode'] = 'round_numbers'

        # visualization code
        df = pd.read_csv('five-year-survival-rates-from-lung-cancer.csv')
        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]
        df1 = df1.sort_values('Lung',ascending = False)

        ax = sns.barplot(x = df1['Entity'], y = df1['Lung'],data=df1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

        #ax = sns.barplot(x = 'Lung', y = 'Entity',data=df1)
        # for index, value in enumerate(df1['Lung']):
        #     print(index,value)
        #     plt.text(value+0.4, index+0.1, int(value),color='black',fontsize=11)
        plt.grid()
        ax.set_xlabel(None)
        ax.set_ylabel(None)
        plt.title("Survival Lung Cancer Rates")
        plt.tight_layout()
        plt.ylim(-1,40)
        plt.xlim(-2,60)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        #plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visLSYear.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visLSYear.html',{})

def visLSCountry(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 6), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code

        df = pd.read_csv('five-year-survival-rates-from-Lung-cancer.csv')

        country = str(request.POST.get('country'))
        # print(country)
        df1 = df[df['Entity'] == country]

        #plt.figure(figsize=(10, 7))
        ax = sns.barplot(x = 'Year', y = 'Lung',data=df1,palette = 'hls')
        ax.tick_params(axis='both', which='major', pad=20)
        ax.tick_params(axis='both', which='minor', pad=20)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        
        ax.set_ylabel(ylabel=None)
        ax.set_xlabel(None)
        plt.title("Survival Lung Cancer Rates in "+country)
        

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visLSCountry.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visLSCountry.html',{})

#Visualization Breast Survival Rates
def visBreastSurvival(request):
    return render(request,'visBreastSurvival.html',{}) 

def visBSTopCY(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 10), dpi=80,facecolor='w', edgecolor='w', constrained_layout=True)
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        # matplotlib.rcParams['axes.titlepad'] = 0   #The offset of the title from the top of the axes, in points. Default is None

        # visualization code
        df = pd.read_csv('five-year-survival-rates-from-breast-cancer.csv')

        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]

        n = int(request.POST.get('topc'))

        df1 = df1.sort_values('Breast',ascending = False)
        df1 = df1.iloc[:n,:]

        ax = sns.barplot(x = 'Breast', y = 'Entity',data=df1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        for index, value in enumerate(df1['Breast']):
            plt.text(value+0.4, index+0.1, int(value),color='black',fontsize=11)
        
        plt.grid()
        # plt.ylabel(ylabel=None)
        # plt.xlabel(None)
        ax.set_ylabel("Countries",fontsize=18)
        ax.set_xlabel("Counts",fontsize=18)
        plt.title("Survival Breast Cancer Rates in Top "+str(n) +" Countries",loc='left')
        plt.ylim(-1,n)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visBSTopCY.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visBSTopCY.html',{})

def visBSYear(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        
        df = pd.read_csv('five-year-survival-rates-from-breast-cancer.csv')
        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]
        df1 = df1.sort_values('Breast',ascending = False)

        ax = sns.barplot(x = df1['Entity'], y = df1['Breast'],data=df1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.grid()
        plt.ylabel("Total Breast Survival Counts")
        plt.title("Survival Breast Cancer Rates")
        plt.ylim(-1,100)
        plt.xlim(-2,60)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visBSYear.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visBSYear.html',{})

def visBSCountry(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 6), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code

        df = pd.read_csv('five-year-survival-rates-from-breast-cancer.csv')
        
        country = str(request.POST.get('country'))
        df1 = df[df['Entity'] == country]

        ax = sns.barplot(x = 'Year', y = 'Breast',data=df1,palette = 'hls')
        ax.tick_params(axis='both', which='major', pad=20)
        ax.tick_params(axis='both', which='minor', pad=20)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        #ax.set_theme(style="whitegrid")

        ax.set_ylabel(ylabel=None)
        ax.set_xlabel(None)
        plt.title("Survival Breast Cancer Rates in "+country)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visBSCountry.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visBSCountry.html',{})

# Visualization Cancer Deaths by Types
def visCancerDeathsTypes(request):
    return render(request,'visCancerDeathsTypes.html',{}) 

def visCDTypesC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 6), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        print(type(random))
        # visualization code
        df = pd.read_csv('total_cancer_deaths_by_type_mine_cleandata.csv')
        color =["hotpink","crimson","skyblue",'mediumvioletred','#8f9805','lime','seagreen','firebrick','#F3A0F2','#2CBDFE','#F5B14C','#9D2EC5','#47DBCD']
        
        country = str(request.POST.get('country'))
        df1 = df[df['Entity'] == country]
        df1 = df1.set_index('Year')
        df1.iloc[:,2].plot.line(title='Cancer Deaths in '+str(country),color=rn.sample(color,1),marker='o')
        # plt.ylim(-1,16)
        plt.xlim(1988,2020)  

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visCDTypesC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTypesC.html',{})

def visCDTypesTC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 6), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('total_cancer_deaths_by_type_mine_cleandata.csv')
        color =["hotpink","crimson","skyblue",'mediumvioletred','#8f9805','lime','seagreen','firebrick','#F3A0F2','#2CBDFE','#F5B14C','#9D2EC5','#47DBCD']


        country = str(request.POST.get('country'))
        ct = str(request.POST.get('ctype'))
        df1 = df[df['Entity'] == country]

        df1 = df1.set_index('Year')

        ax = df1.loc[:,ct].plot.line(title='Cancer Deaths in '+str(country)+' due to \n'+ct,color=rn.sample(color,1))
        ax.set_xlabel("Years")
        ax.set_ylabel('No. of deaths')
        # plt.ylim(-1,16)
        plt.xlim(1988,2020)  

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png',bbox_inches='tight')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visCDTypesTC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTypesTC.html',{})

def visCDTypes2C(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(15, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('total_cancer_deaths_by_type_mine_cleandata.csv')

        country = str(request.POST.get('country'))
        ct1 = str(request.POST.get('ctype1'))
        ct2 = str(request.POST.get('ctype2'))

        if ct1 == ct2:
            res = "Please Enter different Cancer Types"
            return render(request,'visCDTypes2C.html',{'res':res})

        df1 = df[df['Entity'] == country]
        df1 = df1.set_index('Year')

        ax = df1.loc[:,[ct1,ct2]].plot.line(title='Cancer Deaths in '+str(country))

        ax.set_xlabel("Years")
        ax.set_ylabel('No. of deaths')
        # plt.ylim(-1,16)
        plt.xlim(1988,2020)  
        plt.tight_layout()
        

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png',bbox_inches='tight')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visCDTypes2C.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTypes2C.html',{})

def visCDTopY(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code

        df = pd.read_csv('total_cancer_deaths_by_type_mine_cleandata.csv')

        y = int(request.POST.get('year'))
        df1 = df[df['Year'] == y]
        df1 = df1.set_index("Entity")
        cancertype = str(request.POST.get('ctype'))
        df1 = df1.sort_values(cancertype,ascending = False)
        df1 = df1.iloc[1:11,:]

        ax = sns.barplot(x=df1.index, y=df1[cancertype],palette="Blues_d")
        plt.title(str(cancertype)+" Deaths in Top 10 Countries")
        plt.ylabel("")
        plt.xlabel("Countries")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        # plt.ylim(-1,16)
        plt.xlim(-4,13)


        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        #response = HttpResponse(buf.getvalue(), content_type='image/png')
        #return response
        return render(request, 'visCDTopY.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTopY.html',{})

def visCDTopCancers(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code

        df = pd.read_csv('total_cancer_deaths_by_type_mine_cleandata.csv')
        df1 = df[df['Entity'] == 'World']
        df2 = df1.sum(axis=0)
        df2 = df2.iloc[3:]
        df2 = df2.sort_values(ascending= False)
        df2 = pd.DataFrame(df2)
        df2['cancerstypes'] = df2.index

        # Changing columns name 
        df2.columns = ['Numbers', 'Cancer']

        n = int(request.POST.get('num'))
        # ax = sns.barplot(x="Numbers", y="Cancer", data=df2.iloc[:n,:] )
        ax = sns.barplot(x="Cancer", y = "Numbers",data=df2.iloc[:n,:])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right',fontsize=10)
        ax.set_ylabel('Data (in millions)')
        ax.set_title("Cancer Deaths All Over World \n (From 1990 - 2017) ",fontsize=12, fontweight='bold')
        plt.ylim(-1,50000000)
        # plt.xlim(-3,30)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDTopCancers.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTopCancers.html',{})

# Visualization Cancer Deaths attributed to Tobacco
def visCancerDeathsTobacco(request):
    return render(request,'visCancerDeathsTobacco.html',{}) 

def visCDTYearCountries(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('share-of-cancer-deaths-attributed-to-tobacco_mine_dataclean.csv')
        c1 = str(request.POST.get('c1'))
        c2 = str(request.POST.get('c2'))
        c3 = str(request.POST.get('c3'))
        c4 = str(request.POST.get('c4'))

        if c1==c2 or c2==c3 or c3==c4 or c4==c1 or c1==c3 or c2==c4 :
            res = "Please Select Different Countries"
            return render(request,'visCDTYearCountries.html',{'res':res})

        df1=df[df['Entity'].isin([c1,c2,c3,c4])]

        sns.lineplot(data=df1, x="Year", y="AgeS-cancer deaths-tobacco", hue="Entity",marker="o")
        plt.title("AGE-STANDARDIZED SHARE OF CANCER DEATHS ATTRIBUTED TO TOBACCO")
        plt.xlim(1988,2019)
        # plt.ylim(0,700000)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDTYearCountries.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTYearCountries.html',{})

    return render(request,'visCDTYearCountries.html',{})

def visCDTTopC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 11
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('share-of-cancer-deaths-attributed-to-tobacco_mine_dataclean.csv')
        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]
        n = int(request.POST.get('top'))

        df1 = df1.sort_values('AgeS-cancer deaths-tobacco',ascending = False)
        df1 = df1.iloc[:n,:]

        ax = sns.barplot(x="Entity", y="AgeS-cancer deaths-tobacco",data=df1)
        plt.title("Data of Top "+str(n)+" Countries \nAGE-Standardized Share of Cancer Deaths Attributed To Tobacoo\n in "+str(yr)+" Year")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        plt.ylim(0,90)
        # plt.xlim(-3,16)
        
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDTTopC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTTopC.html',{})

def visCDTBottomC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 11
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('share-of-cancer-deaths-attributed-to-tobacco_mine_dataclean.csv')
        yr = int(request.POST.get('year'))
        df1 = df[df['Year'] == yr]
        n = int(request.POST.get('bottom'))

        df1 = df1.sort_values('AgeS-cancer deaths-tobacco',ascending = True)
        df1 = df1.iloc[:n,:]

        ax = sns.barplot(x="Entity", y="AgeS-cancer deaths-tobacco",data=df1)
        plt.title("Data of Bottom "+str(n)+" Countries \nAGE-Standardized Share of Cancer Deaths Attributed To Tobacoo\n in "+str(yr)+" Year")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        plt.ylim(0,6)
        # plt.xlim(-3,16)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDTBottomC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTBottomC.html',{})

def visCDTpC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 11
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('share-of-cancer-deaths-attributed-to-tobacco_mine_dataclean.csv')
        country = str(request.POST.get('c'))
        df1 = df[df["Entity"] == country]
        ax = sns.barplot(data=df1, x="Year", y="AgeS-cancer deaths-tobacco")
        plt.title("AGE-Standardized Share of Cancer Deaths Attributed To Tobacoo\n"+ "in "+str(country))
        ax.set_ylabel(None)
        ax.set_xlabel("Years")
        # plt.ylim(0,17)
        plt.xlim(-3,9)
        
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDTpC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDTpC.html',{})

def visCDT2C(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 7), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('share-of-cancer-deaths-attributed-to-tobacco_mine_dataclean.csv')
        c1 = str(request.POST.get('c1'))
        c2 = str(request.POST.get('c2'))

        if c1 == c2:
            res = "Select Different Countries"
            return render(request,'visCDT2C.html',{'res':res})
        df1=df[df['Entity'].isin([c1,c2])]

        sns.barplot(x="Year", y="AgeS-cancer deaths-tobacco", hue="Entity", data=df1, ci=None)
        plt.title("CANCER DEATHS ATTRIBUTED TO TOBACCO \n in "+str(c1)+" and "+str(c2))
        plt.xlim(-3,9)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDT2C.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDT2C.html',{})

# Visualization Cancer deaths by Age Group
def visCancerDeathsAge(request):
    return render(request,'visCancerDeathsAge.html',{})

def visCDAageGC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 5), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('cancer-deaths-by-age_mine_cleandata.csv')

        country = str(request.POST.get('c'))
        agegroup = str(request.POST.get('agegroup'))
        df1 = df[df["Entity"] == country]
        ax = sns.barplot(y=df[agegroup], x = df1['Year'], data = df1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.set_title("Cancer deaths of "+str(agegroup)+ ' in '+str(country) )
        ax.set_ylabel(ylabel=None)
        plt.xlim(-2,28)
        # plt.ylim(0,700000)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDAageGC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDAageGC.html',{})

def visCDApY(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 5), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('cancer-deaths-by-age_mine_cleandata.csv')
        df1 = df[df['Entity'] == "World"]

        year = int(request.POST.get('year'))
        df1 = df1[df1["Year"] == year]

        df2 = df1.T
        df2 = df2.iloc[3:,:]
        df2['Age'] = df2.index

        df2.columns = ['Count',"Age"]

        ax = sns.barplot(x="Count",y = "Age" ,data = df2, palette="husl" )
        ax.set_title("Cancer death Rates by Age in Year "+str(year))
        ax.set_ylabel(ylabel=None) 
        ax.set_xlabel("Numbers in million")
        
        plt.xlim(-2,5000000)
        plt.ylim(-1,5)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDApY.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDApY.html',{})

def visCDAsyey(request):
    if request.method=='POST':
        # settings for the graph
        fig=plt.figure(figsize=(12, 5), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        # visualization code
        df = pd.read_csv('cancer-deaths-by-age_mine_cleandata.csv')

        country = str(request.POST.get('country'))
        df1 = df[df['Entity'] == country]

        y1 = int(request.POST.get('y1'))
        y2 = int(request.POST.get('y2'))
        if (y1>y2):
            res = 'Start Year should be less than End Year'
            return render(request,'visCDAsyey.html',{'res':res})
        elif y1==y2:
            res = 'Start Year and End Year are Same'
            return render(request,'visCDAsyey.html',{'res':res})

        df1 = df1[(df1["Year"]>=y1) & (df1["Year"]<=y2)]
        df2 = df1.set_index(df1['Year'])
        df2 = df2.iloc[:,3:]
        ax = sns.barplot(data = df2,palette="flare")
        ax.set_title("Cancer death Rates by Age Group\n in "+str(country)+" from "+str(y1)+" to "+str(y2) )
        plt.xlim(-2,7)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visCDAsyey.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visCDAsyey.html',{})

# Visualization Cancer Prevalence by Age
def visNoPeopleByAge(request):
    return render(request,'visNoPeopleByAge.html',{})

def visNPAsyeyC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 5), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('number-of-people-with-cancer-by-age_mine_dataclean.csv')

        country = str(request.POST.get('c'))
        df1=df[df['Entity']== country]

        sy = int(request.POST.get('startyear'))
        ey = int(request.POST.get('endyear'))

        if (sy>ey):
            res = 'Start Year should be less than End Year'
            return render(request,'visNPAsyeyC.html',{'res':res})
        elif sy==ey:
            res = 'Start Year and End Year are Same'
            return render(request,'visNPAsyeyC.html',{'res':res})

        df1 = df1[(df1['Year'] >= sy) & (df1['Year'] <= ey)]

        df1=df1.set_index('Year')
        temp = df1.iloc[-1,1:].max()
        t = temp/10
        #df1.iloc[:,1:].plot.line(marker="o")
        sns.lineplot(data=df1,palette='hls',linewidth = 2)
        plt.title("Cancer Prevalence by Age in "+str(country))

        plt.xlim(sy,ey)
        plt.ylim(-20,temp+t)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visNPAsyeyC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visNPAsyeyC.html',{})

def visNPAsubplotC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(10, 5), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('number-of-people-with-cancer-by-age_mine_dataclean.csv')

        country = str(request.POST.get('c'))
        df1=df[df['Entity']== country]

        fig, axes = plt.subplots(2, 2, figsize=(15, 5), sharex=True, constrained_layout=True)
        fig.suptitle("Cancer prevalence by age in "+str(country),y = 1,x=0.5)
        
        sns.set_palette("dark")

        sns.lineplot(ax=axes[0,0], data=df1, x='Year', y="Age: 5-14 years")
        axes[0,0].set_title("Age: 5-14 years", fontsize=12)
        axes[0,0].set_ylabel(None)

        sns.lineplot(ax=axes[0,1],data=df1, x='Year', y="Age: 15-49 years")
        axes[0,1].set_title("Age: 15-49 years", fontsize=12)
        axes[0,1].set_ylabel(None)

        sns.lineplot(ax=axes[1,0],data=df1, x='Year', y="Age: 50-69 years")
        axes[1,0].set_title("Age: 50-69 years", fontsize=12)
        axes[1,0].set_ylabel(None)

        sns.lineplot(ax=axes[1,1], data=df1, x='Year', y="Age: 70+ years")
        axes[1,1].set_title("Age: 70+ years", fontsize=12)
        axes[1,1].set_ylabel(None)

        custom_xlim = (1988, 2020)
        custom_ylim = (None,None)

        # Setting the values for all axes.
        plt.setp(axes, xlim=custom_xlim, ylim=custom_ylim)

        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visNPAsubplotC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visNPAsubplotC.html',{})

def visNPAareaC(request):
    if request.method=='POST':
        # CODE HERE settings 
        fig=plt.figure(figsize=(12, 5), dpi=85,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 9
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        
        # visualization code
        df = pd.read_csv('cancer-deaths-by-age_mine_cleandata.csv')

        country = str(request.POST.get('c'))
        df1=df[df['Entity']== country]
        
        x = df1.iloc[:,2]
        
        plt.stackplot(x,df1.iloc[:,2],df1.iloc[:,3],df1.iloc[:,4],df1.iloc[:,5],df1.iloc[:,6],labels=['Age: Under 5', 'Age: 5-14 years','Age: 15-49 years', 'Age: 50-69 years', 'Age: 70+ years'])
        plt.legend(loc='upper left')
        sns.set_palette("RdPu")
        plt.title("Prevalence of Cancer by Age, "+str(country)+", 1990 to 2017",fontsize=15,pad=10)
        plt.ylabel("In Billions")
        xlim(1990,2017)
        
        # Saving an image 
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.tight_layout()
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()

        graphic = base64.b64encode(buffercontent) 
        return render(request, 'visNPAareaC.html', {'graphic': graphic.decode('utf8')})

    else:
        return render(request,'visNPAareaC.html',{})


# Prediction 
def lungsprediction(request):
    if request.method == 'POST':        
        dataset=pd.read_csv('lung_cancer_examples.csv')        
        X = dataset.iloc[:,2:-1].values
        Y = dataset.iloc[:,-1].values
        X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25,random_state=0)
        age=request.POST.get("age")                      # getting all the values from the form
        smokes=request.POST.get("smoke")
        areaq=request.POST.get("areaq")
        alcohol=request.POST.get("alcohol")
        print("before",X_test.shape)               
        X_test=np.append(X_test,[[age,smokes,areaq,alcohol]],axis=0) #appending the entered data into test dataset in last row
        print("after",X_test.shape)
        sc=StandardScaler()                            # preprocessing the entered data
        X_train=sc.fit_transform(X_train)
        X_test=sc.transform(X_test)
        model = pickle.load(open('lungs_model_new.sav', 'rb'))
        Y_predict=model.predict(X_test)                 # making the prediction
        l=len(Y_predict)
        print("prediction",Y_predict[l-1])         
        if(Y_predict[l-1]==0):                         # checking the result of last row only.
            a = 1
            return render(request,'doctorF/lungsprediction.html',{"ans":a})
        elif(Y_predict[l-1]==1):
            a = 2
            return render(request,'doctorF/lungsprediction.html',{"ans":a})

    return render(request,'doctorF/lungsprediction.html',{})

def prostateprediction(request):
    if request.method == 'POST':
        dataset=pd.read_csv('Prostate_Cancer.csv')
        X = dataset.iloc[:,[2,3,4,5,6,7,8,9]].values
        Y = dataset.iloc[:,1].values
        X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25,random_state=0)
        radius=request.POST.get("radius")
        texture=request.POST.get("texture")
        perimeter=request.POST.get("peri")
        area=request.POST.get("area")
        smoothness=request.POST.get("smoot")
        compactness=request.POST.get("compact")
        symmetry=request.POST.get("symmetry")
        fractaldimension=request.POST.get("fd")
        print("before",X_test.shape)
        X_test=np.append(X_test,[[radius,texture,perimeter,area,smoothness,compactness,symmetry,fractaldimension]],axis=0)
        print("after",X_test.shape)
        sc=StandardScaler()
        X_train=sc.fit_transform(X_train)
        X_test=sc.transform(X_test)
        model= pickle.load(open('prostate_model_new.sav', 'rb'))
        Y_predict=model.predict(X_test)
        l=len(Y_predict)
        print("prediction",Y_predict[l-1])
        if(Y_predict[l-1]==0):
            a = 1
            return render(request,'doctorF/prostateprediction.html',{"ans":a})
        elif(Y_predict[l-1]==1):
            a = 2
            return render(request,'doctorF/prostateprediction.html',{"ans":a})

    return render(request,'doctorF/prostateprediction.html',{})

    

# Image Prediction
def upload_file(f,name):
    destination = open("media/"+name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def handle_uploaded_file(f,name):
    destination = open(name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def breastpredictionDL(request):
    if request.method == "POST":
        f = request.FILES['predfile'] # getting the file from form tag

        # code to check that file format should be png or jpg only
        if (request.FILES["predfile"].content_type != 'image/jpeg') or (request.FILES["predfile"].content_type != 'image/png'):
            invalid = 'Please submit jpg or png Image'
            return render(request,'doctorF/breastpredictionDL.html',{'invalid':invalid})

        handle_uploaded_file(f,f.name)
        classifier = load_model('breast_cnn_model.h5',compile=False) # calling the trained Deep learning model

        test_image =image.load_img(f.name,target_size =(64,64))  ## Upload the image here 
        # preprocessing the image before making prediction
        test_image =image.img_to_array(test_image)         
        test_image =np.expand_dims(test_image, axis =0)
        result = classifier.predict(test_image)   # getting the predictions
        
        if result[0][0] >= 0.5:              
            prediction = 'Benin'
            pred = 1
        elif result[0][1] >= 0.5:
            prediction = 'Malignant'
            pred = 2
        else:
            pred = 3
            prediction = 'Normal'
        
        return render(request,'doctorF/breastpredictionDL.html',{'ans':pred})

    return render(request,'doctorF/breastpredictionDL.html',{})

def skinpredictionDL(request):
    if request.method == "POST":

        f = request.FILES['predfile'] # here you get the files needed
        
        if (request.FILES["predfile"].content_type != 'image/jpeg') or (request.FILES["predfile"].content_type != 'image/png'):
            invalid = 'Please submit jpg or png Image'
            return render(request,'doctorF/skinpredictionDL.html',{'invalid':invalid})


        handle_uploaded_file(f,f.name)

        classifier = load_model('skincancer_cnn_model.h5',compile=False)

        test_image =image.load_img(f.name,target_size =(64,64))  ## Upload the image here 
        test_image =image.img_to_array(test_image)
        test_image =np.expand_dims(test_image, axis =0)
        result = classifier.predict(test_image)
        print(result)

        if result[0][0] >= 0.5:
            prediction = 'Maligant'
            pred = 1
        else:
            prediction = 'Benign'
            pred = 2
        print(prediction)
        
        return render(request,'doctorF/skinpredictionDL.html',{'ans':pred})

    return render(request,'doctorF/skinpredictionDL.html',{})

def lungpredictionDL(request):
    if request.method == "POST":

        f = request.FILES['predfile'] # here you get the files needed

        if (request.FILES["predfile"].content_type != 'image/jpeg') or (request.FILES["predfile"].content_type != 'image/png'):
            invalid = 'Please submit jpg or png Image'
            return render(request,'doctorF/lungpredictionDL.html',{'invalid':invalid})

        handle_uploaded_file(f,f.name)

        classifier = load_model('lung_cnn_model.h5',compile=False)

        test_image =image.load_img(f.name,target_size =(64,64))  ## Upload the image here 
        test_image =image.img_to_array(test_image)
        test_image =np.expand_dims(test_image, axis =0)
        result = classifier.predict(test_image)
        print(result)

        if result[0][0] >= 0.5:
            prediction = 'adenocarcinoma'
            pred = 1
            print(type(pred))
        elif result[0][1] >= 0.5:
            prediction = 'large.cell.carcinoma'
            pred = 2
        elif result[0][2] >= 0.5:
            prediction = 'Normal - No Lung Cancer'
            pred = 3
        else:
            prediction = 'squamous.cell.carcinoma'
            pred = 4
            
        return render(request,'doctorF/lungpredictionDL.html',{'ans':pred})

    return render(request,'doctorF/lungpredictionDL.html',{})


# Static Pages Linkied with Index
def breastcancer(request):
    return render(request,'breastcancer.html',{})

def lungcancer(request):
    return render(request,'lungcancer.html',{})

def cervicalcancer(request):
    return render(request,'cervicalcancer.html',{})

def prostatecancer(request):
    return render(request,'prostatecancer.html',{})

def loweryourriskofcancer(request):
    return render(request,'loweryourriskofcancer.html',{})

def copingwithcancer(request):
    return render(request,'copingwithcancer.html',{})

def yourgenes(request):
    return render(request,'yourgenes.html',{})