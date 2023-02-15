from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def RegistrationInterface(request):
  try:
    admin = request.session['admin']
    print("ADMIN:", admin)
    return render(request,"doctorregistration.html",{'msg':''})
  except Exception as e:
    print(e)
    return render(request, "AdminLogin.html", {'msg': ''})
@xframe_options_exempt
def RegistrationDisplayAll(request):
  try:
    admin = request.session['admin']
    print("ADMIN:", admin)
    db,cmd = Pool.ConnectionPooling()
    q = "Select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization) as tspecialization  from doctor D"
    cmd.execute(q)
    records=cmd.fetchall()
    print(records)
    db.close()
    return render(request,"DisplayAllRegistration.html",{'result':records,'msg':''})
  except Exception as e:
    print(e)
    return render(request, "AdminLogin.html",{'msg':''})

@xframe_options_exempt
def UpdateRegistration(request):
  try:
    db,cmd=Pool.ConnectionPooling()
    doctorid=request.GET['did']
    doctorname = request.GET['doctorname']
    dob = request.GET['dob']
    gender = request.GET['gender']
    number = request.GET['mobileno']
    email = request.GET['email']
    specialization = request.GET['specialization']

    q="update doctor set doctorname='{1}',specialization='{2}',email='{3}',mobileno='{4}',dob='{5}',gender='{6}' where doctorid={0}".format(doctorid,doctorname,specialization,email,number,dob,gender)
    cmd.execute(q)
    db.commit()
    db.close()
    return JsonResponse({'result':True,},safe=False)
  except Exception as e:
    print(e)
    return JsonResponse({'result': False,}, safe=False)

@xframe_options_exempt
def DeleteRegistration(request):
  try:
    db,cmd=Pool.ConnectionPooling()
    doctorid =request.GET['doctorid']

    q="delete from doctor where doctorid={0}".format(doctorid)
    cmd.execute(q)
    db.commit()
    db.close()
    return JsonResponse({'result': True,}, safe=False)
  except Exception as e:
    print(e)
    return JsonResponse({'result': False,}, safe=False)

@xframe_options_exempt
def RegistrationSubmit(request):
   try:
     db,cmd=Pool.ConnectionPooling()
     doctorname=request.POST['doctorname']
     dob = request.POST['dob']
     gender = request.POST['gen']
     number = request.POST['number']
     email = request.POST['email']
     specialization = request.POST['specialization']
     iconfile = request.FILES['icon']

     q="insert into doctor(doctorname,dob,gender,mobileno,email,specialization,picture) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(doctorname,dob,gender,number,email,specialization,iconfile.name)

     print(q)
     cmd.execute(q)
     db.commit()
     F=open("d:/medassist/assets/"+iconfile.name,"wb")
     for chunk in iconfile.chunks():
        F.write(chunk)
     F.close()
     db.close()
     return render(request, "doctorregistration.html", {'msg': 'Record Submitted'})
   except Exception as e:
     print(e)
     return render(request, "doctorregistration.html", {'msg': 'Fail to Submit Record'})

@xframe_options_exempt
def EditregistrationPicture(request):
    try:
      db,cmd=Pool.ConnectionPooling()
      doctorid = request.POST['doctorid']
      iconfile = request.FILES['icon']

      q = "update doctor set picture='{0}' where doctorid={1}".format(iconfile.name, doctorid)
      cmd.execute(q)
      db.commit()
      F = open("d:/medassist/assets/"+iconfile.name,"wb")
      for chunk in iconfile.chunks():
        F.write(chunk)
      F.close()
      db.close()

      return JsonResponse({"result": True,}, safe=False)
    except Exception as e:
      print(e)
      return JsonResponse({"result": False,}, safe=False)

