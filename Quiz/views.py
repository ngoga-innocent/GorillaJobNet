from django.shortcuts import render
from .models import Faculties,Question,Quiz,Answer,UserSubmission
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from Payment.CheckExamPaid import CheckUserSubscription,CheckUserPayment,CheckOTP
from django.contrib.auth.models import User
from Payment.models import OTP
# Create your views here.
def quizHome(request):
    context = {} 
    query=request.GET.get('query','')
    if query:
        results=Faculties.objects.filter(name__icontains=query)[:10]
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            faculties_list = [
            {
                "name": faculty.name,
                "thumbnail": faculty.thumbnail.url if faculty.thumbnail else None,
                "id": faculty.id,
                "description": faculty.description,
                "quiz_count": faculty.get_faculty_quizzes().count()
            }
            for faculty in results
        ]
        return JsonResponse({"faculties": faculties_list}, status=200)
    else:
        results=Faculties.objects.all()
        context={'faculties': results}
        
          
    return render(request, 'home.html',context)
# @login_required(login_url='/account')
def FaculityQuizes(request,pk):
    quizes=Quiz.objects.filter(faculty=pk)
    context={"quizes":quizes}
    return render(request, 'Quizes.html',context)

# @login_required(login_url='/account/')
def CheckUserPaidExam(request): 
    otp=request.GET.get('otp')
    if request.user.is_authenticated and otp:
        user=User.objects.get(pk=request.user.id)
        exam_id=request.GET.get('exam_id')
        if CheckUserPayment(user.id,otp) or CheckUserSubscription(user.id):
            return JsonResponse({"paid":True},status=200)
        else: return JsonResponse({"paid":False},status=200)
    else:return JsonResponse({"paid":False},status=200)
def verifyCode(request):
    code=request.GET.get('code')
    return JsonResponse({"valid":CheckOTP(code)})          
    
    # print (user.id, exam_id)

  
    
# @login_required(login_url='/account/')
def QuizQuestions(request,pk):
    try:
        quiz=get_object_or_404(Quiz,pk=pk)
        questions=quiz.get_quiz_questions()
        # paginator = Paginator(question, 50)
        # page_number = request.GET.get("page")
        # page_obj = paginator.get_page(page_number)
        context={"questions":questions}
        return render(request,'questions.html',context)
    except Question.DoesNotExist:
        return render(request,'404.html') 
def SearchDepartent(request):
    query=request.GET.get('query','')
    results=Faculties.objects.filter(name__icontains=query)[:10]
    context={"results":results}
    return render(request,'search.html',context) 
# @login_required(login_url='/account/')
def SubmitUserResponse(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_response = request.POST.get('answer_id')
        code=request.POST.get('code')
        user=request.user
        
        try:
            question=Question.objects.get(id=question_id)
        
            quiz=question.quiz
            answer=Answer.objects.get(id=user_response)
            if not answer:
                return JsonResponse({"status": "error"}, status=200)
            if answer and answer.correct:
                correct=True
            else:
                correct=False
            try:
                code=OTP.objects.get(otp=code)
                ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
                if request.user.is_authenticated:
                    user_done_question=UserSubmission.objects.get(code=code,user=user,question=question_id,created_on__gte=ten_minutes_ago)
                else:
                    user_done_question=UserSubmission.objects.get(code=code,question=question_id,created_on__gte=ten_minutes_ago)    
                user_done_question.user_response=answer
                user_done_question.correct=correct
                user_done_question.save()
                return JsonResponse({"status": "success"}, status=200)
                
            except UserSubmission.DoesNotExist:            
                if request.user.is_authenticated:
                    user_answer=UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,user=user,code=code,correct=correct)
                else:
                    user_answer=UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,code=code,correct=correct)    

                if user_answer:
                    return JsonResponse({"status": "success"}, status=200)
                else:
                    print(user_answer)
                    return JsonResponse({"status": "error to create"}, status=400)
        except Answer.DoesNotExist:
            return JsonResponse({"status": "choose one please"}, status=200)        
# @login_required(login_url='/account/')
def GetAnswer(request,id):
   
    user_id = request.user.id
    otp=request.GET.get('otp')
    if CheckOTP(otp):
        try:
            quiz=Quiz.objects.get(id=id)
            Otp=OTP.objects.get(otp=otp)
            # print(quiz.id)
            number_of_question=len(quiz.get_quiz_questions())
            # print(number_of_question)
            ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
            
            user_submission=UserSubmission.objects.filter(code=Otp,quiz=quiz,created_on__gte=ten_minutes_ago)
            correct_answer=0
            for submission in user_submission:
                if submission.correct:
                    correct_answer=correct_answer+1
            marks=0        
            if number_of_question>0:
                marks=correct_answer * 100 /number_of_question
            response_data = {
                        "marks": marks,
                        "status":"success",
                        "quiz_id":quiz.id
                        }     
                
            return JsonResponse(response_data,status=200)
            
        except Quiz.DoesNotExist:
            return JsonResponse({"error":"error"},status=200) 
       

    return JsonResponse({"You are not Allowed to Access This Exam,Please pay first"},status=200)
# @login_required(login_url='/account/')
def GetAllAnswer(request,id):
  
    quiz = get_object_or_404(Quiz, id=id)
    quiz_questions = quiz.get_quiz_questions()
    context = {"quiz_questions": quiz_questions,"quiz_name":quiz.name}
    return render(request, 'answers.html', context) 
        

          


