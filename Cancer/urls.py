"""Cancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""" Hello Eveyrone """""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings # for imprting settings file
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/',views.form,),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('contactus/',views.contactus,name='contactus'),
    path('footer/',views.footer,),
    path('base/',views.base,),

    path('recoverpassword/',views.recoverpassword,name='recoverpassword'),
    path('help/',views.help,name='help'),
    path('editprofile/',views.editprofile, name="editprofile"),
    path('changepassword/',views.changepassword, name="changepassword"),
    path('review/',views.review, name='review'),
    path('sidebar/',views.sidebar,),
    path('logout/',views.logout, name="logout"),
    path('profile/',views.profile, name="profile"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('chatpage/',views.chatpage, name="chatpage" ),
    path('doctorspage/',views.doctorspage,name="doctorspage"),
    path('labs/',views.labs,name="labs"),
    path('hospitals/',views.hospitals,name="hospitals"),
    path('clinics/',views.clinics,name="clinics"),
    path('userappointment/<int:id>',views.userappointment,name="userappointment"),
    path('userappointmentstatus/',views.userappointmentstatus,name="userappointmentstatus"),

    path('docsidebar/',views.docsidebar,name="docsidebar"),
    path('docprofile/',views.docprofile,name="docprofile"),
    path('doceditprofile/',views.doceditprofile,name="doceditprofile"),
    path('doclogin/',views.doclogin,name="doclogin"),
    path('dochelp/',views.dochelp,name="dochelp"),
    path('docdashboard/',views.docdashboard, name="docdashboard"),
    path('docappointment/',views.docappointment,name="docappointment"),
    path('docchangepassword/',views.docchangepassword,name="docchangepassword"),
    path('docpatients/',views.docpatients,name="docpatients"),
    path('docchatpage/',views.docchatpage,name="docchatpage"),
    path('docchatpage/<int:appid>',views.docchatpage,name="docchatpage"),
    path('get_messages/',views.getmessages, name="getmessages"),
    path('doclogout/',views.doclogout, name="doclogout"),

    path('enabledisbale/', views.enable_disable, name='enable_disable'),
    path('user_chat_upate/', views.user_chat_update, name='chat_update'),
    

    path('test/',views.test, name='test'),

    path('lungsprediction/',views.lungsprediction, name='lungsprediction'),
    path('prostateprediction/',views.prostateprediction, name='prostateprediction'),
    path('breastpredictionDL/',views.breastpredictionDL, name='breastpredictionDL'),
    path('skinpredictionDL/',views.skinpredictionDL,name="skinpredictionDL"),
    path('lungpredictionDL/',views.lungpredictionDL,name="lungpredictionDL"),

    path('visLungSurvival/',views.visLungSurvival, name='visLungSurvival'),
    path('visLSYear/',views.visLSYear, name='visLSYear'),
    path('visLSTopCY/',views.visLSTopCY, name='visLSTopCY'),
    path('visLSCountry/',views.visLSCountry, name="visLSCountry"),

    path('visBreastSurvival/',views.visBreastSurvival, name='visBreastSurvival'),
    path('visBSYear/',views.visBSYear, name='visBSYear'),
    path('visBSTopCY/',views.visBSTopCY, name='visBSTopCY'),
    path('visBSCountry/',views.visBSCountry, name="visBSCountry"),

    path('visCancerDeathsTypes/',views.visCancerDeathsTypes, name='visCancerDeathsTypes'),
    path('visCDTypesC/',views.visCDTypesC, name="visCDTypesC"),
    path('visCDTypesTC/',views.visCDTypesTC, name="visCDTypesTC"),
    path('visCDTypes2C/',views.visCDTypes2C, name="visCDTypes2C"),
    path('visCDTopY/',views.visCDTopY, name="visCDTopY"),  
    path('visCDTopCancers/',views.visCDTopCancers, name="visCDTopCancers"),

    path('visCancerDeathsTobacco/',views.visCancerDeathsTobacco, name="visCancerDeathsTobacco"),
    path('visCDTYearCountries/',views.visCDTYearCountries, name="visCDTYearCountries"),
    path('visCDTTopC/',views.visCDTTopC, name="visCDTTopC"),
    path('visCDTBottomC/',views.visCDTBottomC, name="visCDTBottomC"),
    path('visCDTpC/',views.visCDTpC, name="visCDTpC"),
    path('visCDT2C/',views.visCDT2C, name="visCDT2C"),

    path('visCancerDeathsAge/',views.visCancerDeathsAge, name="visCancerDeathsAge"),
    path('visCDAageGC/',views.visCDAageGC,name="visCDAageGC"),
    path('visCDApY/',views.visCDApY,name="visCDApY"),
    path('visCDAsyey/',views.visCDAsyey, name="visCDAsyey"),

    path('breastcancer/',views.breastcancer,name="breastcancer"),
    path('lungcancer/',views.lungcancer,name="lungcancer"),
    path('cervicalcancer/',views.cervicalcancer, name="cervicalcancer"),
    path('prostatecancer/',views.prostatecancer, name="prostatecancer"),

    path('loweryourriskofcancer/',views.loweryourriskofcancer, name="loweryourriskofcancer"),
    path('copingwithcancer/',views.copingwithcancer,name="copingwithcancer"),
    path('yourgenes/',views.yourgenes,name="yourgenes"),


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
