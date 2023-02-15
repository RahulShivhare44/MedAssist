from django.shortcuts import render
from . import Pool
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def SubQuestionInterface(request):
    try:
        admin = request.session['admin']
        print("ADMIN:", admin)
        return render(request,'SubQuestions.html',{'msg':''})
    except Exception as e:
        print(e)
        return render(request, "AdminLogin.html", {'msg': ''})
@xframe_options_exempt
def SubQuestionSubmit(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        subquestionno=request.GET['subquestionno']
        specialization=request.GET['specialization']
        question=request.GET['question']
        subquestion=request.GET['subquestion']

        q="insert into subquestions(subquestionnumber,specializationid,questionid,subquestion) value({0},{1},{2},'{3}')".format(subquestionno,specialization,question,subquestion)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,'SubQuestions.html',{'msg':"Record Submitted"})
    except Exception as e:
        print(e)
        return render(request,'SubQuestions.html',{'msg':'Fail to Record Submit'})




