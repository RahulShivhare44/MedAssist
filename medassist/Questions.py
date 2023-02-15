from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def QuestionInterface(request):
    try:
        admin = request.session['admin']
        print("ADMIN:", admin)
        return render(request,'Questions.html',{'msg':''})
    except Exception as e:
        print(e)
        return render(request, "AdminLogin.html", {'msg': ''})
@xframe_options_exempt
def QuestionSubmit(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        questionno=request.GET['questionno']
        specialization=request.GET['specialization']
        question=request.GET['question']

        q="insert into questions(questionnumber,specializationid,question) value({0},{1},'{2}')".format(questionno,specialization,question)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,'Questions.html',{'msg':"Record Submitted"})
    except Exception as e:
        print(e)
        return render(request,'Questions.html',{'msg':'Fail to Record Submit'})

@xframe_options_exempt
def QuestionJSON(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        specializationid=request.GET['specializationid']
        q="select * from questions where specializationid={0}".format(specializationid)
        cmd.execute(q)
        records=cmd.fetchall()
        print(records)
        db.close()
        return JsonResponse({'result':records,},safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'result':{},},safe=False)