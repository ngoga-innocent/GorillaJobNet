from django.shortcuts import render
from .models import Faculties,Question,Quiz,Answer,UserSubmission
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from Payment.CheckExamPaid import CheckUserSubscription,CheckUserPayment
from django.contrib.auth.models import User
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
@login_required(login_url='/account')
def FaculityQuizes(request,pk):
    quizes=Quiz.objects.filter(faculty=pk)
    context={"quizes":quizes}
    return render(request, 'Quizes.html',context)

@login_required(login_url='/account/')
def CheckUserPaidExam(request):
    user=User.objects.get(pk=request.user.id)
    # exam_id=request.GET.get('exam_id')
    # print (user.id, exam_id)

  
    if CheckUserPayment(user.id) or CheckUserSubscription(user.id):
        return JsonResponse({"paid":True},status=200)
    else: return JsonResponse({"paid":False},status=200)
@login_required(login_url='/account/')
def QuizQuestions(request,pk):
    try:
        question=Question.objects.filter(quiz=pk)
        paginator = Paginator(question, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context={"page_obj":page_obj}
        return render(request,'questions.html',context)
    except Question.DoesNotExist:
        return render(request,'404.html') 
def SearchDepartent(request):
    query=request.GET.get('query','')
    results=Faculties.objects.filter(name__icontains=query)[:10]
    context={"results":results}
    return render(request,'search.html',context) 
@login_required(login_url='/account/')
def SubmitUserResponse(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_response = request.POST.get('answer_id')
        user=request.user
        question=Question.objects.get(id=question_id)
        quiz=question.quiz
        answer=Answer.objects.get(id=user_response)
        if answer.correct:
            correct=True
        else:
            correct=False
        try:
            ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
            user_done_question=UserSubmission.objects.get(user=user,question=question_id,created_on__gte=ten_minutes_ago)
            user_done_question.user_response=answer
            user_done_question.correct=correct
            user_done_question.save()
            return JsonResponse({"status": "success"}, status=200)
            
        except UserSubmission.DoesNotExist:            
            user_answer=UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,user=user,correct=correct)

            if user_answer:
                return JsonResponse({"status": "success"}, status=200)
            else:
                print(user_answer)
                return JsonResponse({"status": "error to create"}, status=400)
@login_required(login_url='/account/')
def GetAnswer(request,id):
    # quiz_id=request.GET.get('quiz_id')
    try:
        quiz=Quiz.objects.get(id=id)
        print(quiz.id)
        number_of_question=len(quiz.get_quiz_questions())
        print(number_of_question)
        ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
        user_submission=UserSubmission.objects.filter(user=request.user,quiz=quiz,created_on__gte=ten_minutes_ago)
        correct_answer=0
        for submission in user_submission:
            if submission.correct:
                correct_answer=correct_answer+1
        marks=correct_answer * 100 /number_of_question
        response_data = {
                "marks": marks,
                "status":"success",
                "quiz_id":quiz.id
                } 
        #print(correct_answer)
    except Quiz.DoesNotExist:
        return JsonResponse({"error":"error"},status=404)    

    return JsonResponse({"data":response_data},status=200)
@login_required(login_url='/account/')
def GetAllAnswer(request,id):
  
    quiz = get_object_or_404(Quiz, id=id)
    quiz_questions = quiz.get_quiz_questions()
    context = {"quiz_questions": quiz_questions,"quiz_name":quiz.name}
    return render(request, 'answers.html', context) 
        

          


