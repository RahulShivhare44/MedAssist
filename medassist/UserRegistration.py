from django.shortcuts import render,redirect
from . import Pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import random
import json
from datetime import date
import time

def UserRegistrationInterface(request):
    return render(request, "UserRegistration.html", {'msg': ''})

def UserLoginInterface(request):
    return render(request,'UserLoginInterface.html')

def ForgetPassword(request):
    return render(request,'ForgetPassword.html')

def LoginInterface(request):
    return render(request, "LoginPage.html",{'msg':''})

def LoginEmail(request):
    return render(request, "LoginEmail.html",{'msg':''})


@xframe_options_exempt
def UserRegistrationDisplayAll(request):
    try:
        admin = request.session['admin']
        print('ADMIN:', admin)
        db, cmd = Pool.ConnectionPooling()
        q = "Select * From userregistration"
        cmd.execute(q)
        records = cmd.fetchall()
        db.close()
        return render(request, "DisplayAllUserRegistration.html", {'result': records})
    except Exception as e:
        print(e)
        return render(request, "AdminLogin.html", {'msg': {}})


def UserRegistrationSubmit(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        username = request.POST['username']
        usercity = request.POST['sourcecity']
        userstate = request.POST['sourcestate']
        useremail = request.POST['useremail']
        userdob = request.POST['userdob']
        tor = request.POST['tor']
        usernum = request.POST['usernum']
        userpassword = request.POST['userpassword']


        q = "insert into userregistration(username,usercity, useremail, userdob, tor,usernum,userpassword,userstate) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(username, usercity, useremail, userdob, tor,usernum,userpassword,userstate)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "UserRegistration.html", {'msg': 'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "UserRegistration.html", {'msg': 'Fail To Submit Record'})

def stateJSON(request):
        try:
            db, cmd = Pool.ConnectionPooling()
            q = "select * from states"
            cmd.execute(q)
            records = cmd.fetchall()
            print(records)
            db.close()
            return JsonResponse({'result': records, }, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'result': {}, }, safe=False)


def cityJSON(request):
        try:
            db, cmd = Pool.ConnectionPooling()
            stateid = request.GET['stateid']
            q = "select * from city where stateid={0}".format(stateid)
            cmd.execute(q)
            records = cmd.fetchall()
            print(records)
            db.close()
            return JsonResponse({'result': records, }, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'result': {}, }, safe=False)



def OtpPage(request):
    btn=request.POST['btn']

    if (btn=="Login"):
        db, cmd = Pool.ConnectionPooling()
        mobileno = request.POST['mobileno']
        q = "select * from userregistration where usernum='{}'".format(mobileno)
        cmd.execute(q)
        data = cmd.fetchone()

        if (data):
            otp=random.randint(1000,8999)
            print(otp)
            print(data)
            # mob = mobileno.split("-")
            # url = "xxxxxxxx{}{}".format(mob[1], otp)
            # print(url)

            request.session['user']=[data['username'],data['usernum'],data['useremail']]
            return render(request, 'OtpPage.html',{'otp':otp,'msg':''})
        else:
            return render(request, 'LoginPage.html',{'msg':'Invalid Mobile Number'})
    else:
        return render(request, "UserRegistration.html", {'msg': ''})

def CheckOtp(request):
    d1=request.POST['digit1']
    d2=request.POST['digit2']
    d3=request.POST['digit3']
    d4=request.POST['digit4']
    gotp=request.POST['gotp']
    otp=d1+d2+d3+d4
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(gotp)
    print(otp)
    if(gotp==otp):
        return WomacForm(request)
    else:
        return render(request, 'OtpPage.html', {'msg': 'Invalid OTP','otp':gotp})

def UserchoiceCheck(request):

    btn=request.GET['btn']
    if(btn=='Number'):
        return render(request, "LoginPage.html",{'msg':''})
    elif(btn=='Email'):
        return render(request,'LoginEmail.html',{'msg':''})
    else:
        return render(request, "UserRegistration.html", {'msg': ''})

def WomacForm(request):
    try:
        db,cmd= Pool.ConnectionPooling()
        q="select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization) sn from doctor D"
        cmd.execute(q)
        data=cmd.fetchall()
        # print('>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<',data)
        return render(request, "WomacSurveys.html", {'msg': "",'Data':data,'UserName':request.session['user'][0]})
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(e)
        return render(request, "WomacSurveys.html", {'msg': ""})



def CheckEmail(request):
    btn = request.POST['btn']

    if (btn == "Login"):
        db, cmd = Pool.ConnectionPooling()
        email = request.POST['email']
        password= request.POST['userpassword']
        q = "select * from userregistration where useremail='{0}' and userpassword='{1}'".format(email,password)
        cmd.execute(q)
        data = cmd.fetchone()

        if (data):
            print(data)
            request.session['user']=[data['username'],data['usernum'],data['useremail'],data['userid']]
            return WomacForm(request)
        else:
            return render(request, 'LoginEmail.html', {'msg': 'Invalid Email Id and Password'})
    else:
        return render(request, "UserRegistration.html", {'msg': ''})



def SurveyInterface(request):
    try:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        sid=request.POST['sid']
        db, cmd = Pool.ConnectionPooling()
        q = "Select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization ) as ts from doctor D where D.doctorid={0}".format(sid)
        cmd.execute(q)
        doctor = cmd.fetchall()
        print(doctor)
        request.session['doctor']=doctor[0]['doctorid']
        return render(request, "surveyinterface.html", {'doctorname':doctor[0]['doctorname'],'icon':doctor[0]['picture'],'specializationid':doctor[0]['specialization'],'splname':doctor[0]['ts']})
    except Exception as e:
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(e)


def UserQuestionInterface(request):
    try:
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        splid=request.POST['splid']
        db,cmd=Pool.ConnectionPooling()
        q='select * from specialization where specializationid={0} '.format(splid)
        cmd.execute(q)
        data=cmd.fetchone()
        print(data)
        return render(request,'userQuestion.html',{'spl':data})
    except Exception as e:
        print(e)
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        return render(request, 'userQuestion.html', {'spl':[]})

def UserQuestion(request):
    try:
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        spl=request.GET['splid']
        db,cmd=Pool.ConnectionPooling()
        q="select Q.*,group_concat(S.subquestion separator '#' ) as subquestions from medassist.questions Q,medassist.subquestions S where Q.questionid=S.questionid and Q.specializationid={0} and S.specializationid={0}  group by Q.questionid".format(spl)
        cmd.execute(q)
        question=cmd.fetchall()
        print(question)

        return JsonResponse({'result':question},safe=False)
    except Exception as e:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        print(e)
        return JsonResponse({'result':[]},safe=False)

def SubmitScore(request):
    try:
        score=json.loads(request.GET['score'])
        print('xxxxxxxxxxxxxxxxxxxxxxxxx',score)
        today=date.today()
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S",t)
        db,cmd=Pool.ConnectionPooling()
        q = "insert into userdoctor(mobileno,doctorid,currentdate,currenttime) values('{}','{}','{}','{}')".format(request.session['user'][1],request.session['doctor'],today,current_time)
        print(q)
        cmd.execute(q)
        db.commit()
        cmd.execute('SELECT last_insert_id() as userdoctorid')
        row=cmd.fetchone()
        print("IDDDD",row)
        qn=1
        for src in score:
            l=list(map(int,src.values()))
            v=sum(l)
            q="insert into userdiagnose(userdoctorid,questionno,totalscore,maxscore) value({0},{1},{2},{3})".format(row['userdoctorid'],qn,v,len(l)*5)
            cmd.execute(q)
            qn+=1
        db.commit()

        return JsonResponse({'result':True,'username':request.session['user'][0],'mobileno':request.session['user'][1],'email':request.session['user'][2]})
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(e)
        return JsonResponse({'result':False})


def UserCheckPrescription(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        q="select * from prescription where patientid={}".format(request.session['user'][3])
        cmd.execute(q)
        data=cmd.fetchall()
        if(data):
            request.session['userprescription']=data
            return JsonResponse({'result':True})
        else:
            return JsonResponse({'result':False})
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(e)
        return JsonResponse({'result':False})

def UserPrescription(request):
    try:
        return render(request,'UserPrescription.html',{'userprescription':request.session['userprescription']})
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(e)
        return render(request,'UserPrescription.html')

def UserDetails(request):
    try:
        db,cmd=Pool.ConnectionPooling()

        q="select username,useremail,usernum from userregistration where usernum='{}'".format(request.session['user'][1])
        # print(q)
        cmd.execute(q)
        user=cmd.fetchone()
        print('xxxxxxxxxxxxxxxxxxx',user)

        q="select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization) as tspecialization from doctor D where D.doctorid={}".format(request.session['doctor'])
        cmd.execute(q)
        doctor=cmd.fetchone()
        print('xxxxxxxxxxxxxxxxxx',doctor)
        return JsonResponse({'doctor':doctor,'user':user})
    except Exception as e:
        print(e)
        return JsonResponse({'result':''})







