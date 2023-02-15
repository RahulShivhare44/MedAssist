from django.shortcuts import render,redirect
from . import Pool
import random
from django.views.decorators.clickjacking import  xframe_options_exempt
from django.http import JsonResponse
from datetime import date
import json

def DoctorLoginInterface(request):
    return render(request,'DoctorLogin.html')

def DoctorOtpPage(request):
    db, cmd = Pool.ConnectionPooling()
    mobileno = request.POST['mobileno']
    q = "select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization) as tspecialization from doctor D where D.mobileno='{}'".format(mobileno)
    cmd.execute(q)
    data=cmd.fetchone()
    if (data):
        otp=random.randint(1000,8999)
        print(otp)
        print(data)
        request.session['doctor']=[data['doctorname'],data['picture'],data['doctorid'],data['specialization'],data['tspecialization']]
        return render(request, 'DoctorOtp.html',{'otp':otp,'msg':''})
    else:
        return render(request, 'DoctorLogin.html',{'msg':'Invalid Mobile Number'})


def CheckDoctorOtp(request):
    d1=request.POST['digit1']
    d2=request.POST['digit2']
    d3=request.POST['digit3']
    d4=request.POST['digit4']
    gotp=request.POST['gotp']
    otp=d1+d2+d3+d4
    if(gotp==otp):
        return render(request, 'DoctorDashboard.html',{'msg':'','doctorname':request.session['doctor'][0],'picture':request.session['doctor'][1]})
    else:
        return render(request, 'DoctorOtp.html',{'msg':'Invalid OTP','otp':gotp})

def DoctorLogout(request):
    del request.session['doctor']
    return render(request, 'DoctorLogin.html')


@xframe_options_exempt
def PatientInterface(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        q='select U.*,(select US.username from userregistration US where US.usernum=U.mobileno) as username from userdoctor U where U.doctorid={}'.format(request.session['doctor'][2])
        print(q)
        cmd.execute(q)
        data=cmd.fetchall()
        print(data)

        return render(request,'Patient.html',{'result':data,'doctorname':request.session['doctor'][0]})
    except Exception as e:
        print(e)
        return render(request,'Patient.html',{'result':''})


@xframe_options_exempt
def PatientReport(request):
    try:
        userdoctorid=request.POST['userdoctorid']
        print('xxxxxxxxxxxxxx',userdoctorid)

        return render(request,'PatientReport.html',{'userdoctorid':userdoctorid})
    except Exception as e:
        print(e)
        return render(request,'PatientReport.html',{'userdoctorid':''})


def PatientDetails(request):
    try:
        userdoctorid=request.GET['userdoctorid']
        print('xxxxxxxxxxxxxx',userdoctorid)
        db,cmd=Pool.ConnectionPooling()
        q='select U.*,(select UD.mobileno from userdoctor UD where UD.userdoctorid={0}) as usermobile,(select UD.currentdate from userdoctor UD where UD.userdoctorid={0}) as userdate,(select UD.currenttime from userdoctor UD where UD.userdoctorid={0}) as usertime from userdiagnose U where U.userdoctorid={0}'.format(userdoctorid)
        print(q)
        cmd.execute(q)
        data=cmd.fetchall()
        # print(data)
        q = "select Q.*,group_concat(S.subquestion separator '#' ) as subquestions from medassist.questions Q,medassist.subquestions S where Q.questionid=S.questionid and Q.specializationid={0} and S.specializationid={0}  group by Q.questionid".format(request.session['doctor'][3])
        cmd.execute(q)
        question=cmd.fetchall()
        # print(question)

        first=data
        second=question
        j=0
        for i in second:
            for k in i.keys():
                first[j].setdefault(k,i[k])
            j+=1
        # print('xxxxxxxxxx',first)

        q="select username,useremail,userid from userregistration where usernum='{}'".format(first[0]['usermobile'])
        print(q)
        cmd.execute(q)
        user=cmd.fetchone()
        # print('xxxxxxxxxxxxxxxxxxx',user)
        request.session['user']=user['userid']
        return JsonResponse({'result':first,'user':user,'doctorname':request.session['doctor'][0],'specialization':request.session['doctor'][4]})
    except Exception as e:
        print(e)
        return JsonResponse({'result':''})




def PrescriptionSubmit(request):
    try:
        data=json.loads(request.GET['data'])
        print('xxxxxxxxxxx',data)
        today=date.today()
        db, cmd = Pool.ConnectionPooling()
        for data1 in data:
         q="insert into prescription(doctorid,patientid,currentdate,prescription,medicine,frequency) values({0},{1},'{2}','{3}','{4}','{5}')".format(request.session['doctor'][2],request.session['user'],today,data1['instructions'],data1['medicine'],data1['frequency'])
         cmd.execute(q)
         db.commit()

        return JsonResponse({'result':True})
    except Exception as e:
        print(e)
        return JsonResponse({'result':False})





