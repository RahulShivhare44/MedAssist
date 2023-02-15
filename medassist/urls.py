"""medassist URL Configuration

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
from django.contrib import admin
from django.urls import path
from . import Specialization
from . import doctorregistration
from . import Questions
from . import SubQuestions
from . import AdminLogin
from . import UserRegistration
from . import DoctorLogin

urlpatterns = [
    path('admin/', admin.site.urls),

    #Specialization................
    path('specialization/',Specialization.SpecializationInterface),
    path('specializationsubmit',Specialization.SpecializationSubmit),
    path('specializationdisplayall/',Specialization.SpecializationDisplayAll),
    path('specializationdisplayalljson/', Specialization.SpecializationDisplayAllJSON),
    path('updatespecialization/', Specialization.UpdateSpecialization),
    path('deletespecialization/', Specialization.DeleteSpecialization),
    path('editspecializationpicture', Specialization.EditSpecializationPicture),

    #DoctorRegistration................
    path('registration/', doctorregistration.RegistrationInterface),
    path('registrationsubmit', doctorregistration.RegistrationSubmit),
    path('registrationdisplayall/', doctorregistration.RegistrationDisplayAll),
    path('updateregistration/', doctorregistration.UpdateRegistration),
    path('deleteregistration/', doctorregistration.DeleteRegistration),
    path('editregistrationpicture', doctorregistration.EditregistrationPicture),

    #Questions....................
    path('questioninterface/', Questions.QuestionInterface),
    path('questionsubmit/', Questions.QuestionSubmit),
    path('questionjson/', Questions.QuestionJSON),


    #Sub-Questions................
    path('subquestioninterface/', SubQuestions.SubQuestionInterface),
    path('subquestionsubmit/', SubQuestions.SubQuestionSubmit),

    #AdminLogin....................
    path('adminlogin/', AdminLogin.AdminLogin),
    path('dashboard', AdminLogin.CheckAdminLogin),
    path('adminlogout/', AdminLogin.AdminLogout),
    path('home/', AdminLogin.Home),

    # User Details------------------------
    path('userregistration/', UserRegistration.UserRegistrationInterface),
    path('userregistrationsubmit', UserRegistration.UserRegistrationSubmit),
    path('userregistrationdisplayall/', UserRegistration.UserRegistrationDisplayAll),
    path('fetchallstates/', UserRegistration.stateJSON),
    path('fetchallcity/', UserRegistration.cityJSON),
    path('login/', UserRegistration.LoginInterface),
    path('otppage', UserRegistration.OtpPage),
    path('userlogininterface/', UserRegistration.UserLoginInterface),  #MAIN URL
    path('loginby/', UserRegistration.UserchoiceCheck),
    path('forget/', UserRegistration.ForgetPassword),
    path('checkotp', UserRegistration.CheckOtp),
    path('checkemail', UserRegistration.CheckEmail),
    path('womacform/', UserRegistration.WomacForm),
    path('surveyinterface', UserRegistration.SurveyInterface),

    #questions.......................
    path('userquestion/', UserRegistration.UserQuestion),
    path('userquestioninterface', UserRegistration.UserQuestionInterface),
    path('submitscore/', UserRegistration.SubmitScore),
    path('usercheckprescription/', UserRegistration.UserCheckPrescription),
    path('userprescription', UserRegistration.UserPrescription),
    path('userdetails/', UserRegistration.UserDetails),

    #Doctor Login...................
    path('doctorlogin/', DoctorLogin.DoctorLoginInterface),
    path('doctorotp', DoctorLogin.DoctorOtpPage),
    path('checkdoctorotp', DoctorLogin.CheckDoctorOtp),
    path('doctorlogout/', DoctorLogin.DoctorLogout),
    path('patient/', DoctorLogin.PatientInterface),
    path('patientreport', DoctorLogin.PatientReport),
    path('patientdetails/', DoctorLogin.PatientDetails),
    path('prescriptionsubmit/', DoctorLogin.PrescriptionSubmit),

]

