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
from django.template.loader import render_to_string
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
    exam_id=request.GET.get('exam_id')
    questions=Quiz.objects.get(id=exam_id)
    print(questions.number_of_questions)
    return JsonResponse({"paid":False,"question_number":questions.number_of_questions},status=200)
    # otp=request.GET.get('otp')
    # if request.user.is_authenticated and otp:
    #     user=User.objects.get(pk=request.user.id)
    #     exam_id=request.GET.get('exam_id')
    #     if CheckOTP():
    #         return JsonResponse({"paid":True},status=200)
    #     else: return JsonResponse({"paid":False},status=200)
    # else:return JsonResponse({"paid":False},status=200)
def verifyCode(request):
    code=request.GET.get('code')
    return JsonResponse({"valid":CheckOTP(code)})          
    
    # print (user.id, exam_id)

  
    
# @login_required(login_url='/account/')
def QuizQuestions(request,pk):
    try:
        quiz=get_object_or_404(Quiz,pk=pk)
        questions=quiz.get_quiz_questions()
        question_Number=0
        if len(questions)>question_Number:
            has_next=True
        else:
            has_next=False    
        if request.method == 'POST':
            question_id = request.POST.get('question_id')
            user_response = request.POST.get('answer_id')
            code=request.POST.get('code')
            user=request.user
            question_number=request.POST.get('question_number')
              
            print(int(question_number) +1,len(questions),code)
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
                    otp=OTP.objects.get(otp=code)
                    ten_minutes_ago = timezone.now() - timezone.timedelta(minutes=10)
                    if request.user.is_authenticated:
                        user_done_question=UserSubmission.objects.get(code=otp,user=user,question=question_id)
                        user_done_question.user_response=answer
                        user_done_question.correct=correct
                        answer_saved=user_done_question.save()
                        print("answer saved Authenticated",answer_saved)
                        if len(questions) == int(question_number)+1:
                            has_next=False
                            html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)],'has_next':has_next})
                            response={
                             'has_next':has_next,
                             'status':'success',
                             'html':html
                                }
                            return JsonResponse(response)
                        elif int(question_number)+1 >len(questions):
                                return GetAnswer(quiz.id,code)    
                        else:
                            has_next=True 
                            html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)],'has_next':has_next,'page_numner':question_number})
                            response={
                            'html': html,
                            'has_next': has_next,
                            'status':'success'
                            }
                            return JsonResponse(response)
                        
                    else:
                        user_done_question=UserSubmission.objects.get(code=otp,question=question_id)    
                        user_done_question.user_response=answer
                        user_done_question.correct=correct
                        answer_saved=user_done_question.save()
                        print("answer saved not authenicated",answer_saved)
                        if len(questions) ==int(question_number):
                            has_next=False
                            html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)],'has_next':has_next})
                            response={
                             'has_next':has_next,
                             'status':'success',
                             'html':html
                                }
                            return JsonResponse(response)
                        elif int(question_number) >len(questions):
                                return GetAnswer(quiz.id,code)    
                        else:
                            has_next=True 
                            html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)],'has_next':has_next})
                            response={
                            'html': html,
                            'has_next': has_next,
                            'status':'success'
                            }
                            return JsonResponse(response)
                    
                    
                      
                    
                except UserSubmission.DoesNotExist:            
                    if request.user.is_authenticated:
                        submitted=UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,user=user,code=otp,correct=correct)
                        print("not exist authenticated",submitted)
                        if int(question_number)+1 > len(questions):
                            return GetAnswer(quiz.id,code)
                            
                            
                        elif len(questions)==int(question_number) :
                            has_next=False
                            # UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,user=user,code=otp,correct=correct) 
                            html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)],'has_next':has_next})
                            response={
                             'has_next':has_next,
                             'status':'success',
                             'html':html
                            }
                        else:
                             
                             html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)],'has_next':has_next})
                             has_next=True
                             response={
                            'html': html,
                            'has_next': has_next,
                            'status':'success'
                            }   
                        # UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,code=otp,correct=correct)      
                        return  JsonResponse(response) 
                    else:
                        submitted=UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,code=otp,correct=correct)    
                        print("not exist not authenticated",submitted)
                        if int(question_number)+1 >len(questions):
                            return GetAnswer(quiz.id,code)
                            
                        elif len(questions)==int(question_number) + 1:
                            has_next=False
                            response={
                             'has_next':has_next,
                             'status':'success'
                            }
                        else:
                             html = render_to_string('quiz_question_partial.html', {'question': questions[int(question_number)+1],'has_next':has_next})
                             has_next=True
                             response={
                            'html': html,
                            'has_next': has_next,
                            'status':'success'
                            }   
                        # UserSubmission.objects.create(user_response=answer,quiz=quiz, question=question,code=otp,correct=correct)      
                        return  JsonResponse(response) 
                   
            except Answer.DoesNotExist:
                return JsonResponse({"status": "choose one please"}, status=200)  
        
        context={"question":questions[question_Number],"has_next":has_next}
        return render(request,'questions.html',context)
    except Question.DoesNotExist:
        return render(request,'404.html') 
def SearchDepartent(request):
    query=request.GET.get('query','')
    results=Faculties.objects.filter(name__icontains=query)[:10]
    context={"results":results}
    return render(request,'search.html',context) 
# @login_required(login_url='/account/')

def GetAnswer(id,otp):
   
    # user_id = request.user.id
    # otp=request.GET.get('otp')
    # print(CheckOTP)
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
                        "marks": round(marks,2),
                        "status":"success",
                        "quiz_id":quiz.id
                        }     
            if Otp.type == 'one':
                Otp.valid=False
                Otp.save() 
            elif timezone.now()>Otp.end_validated_date:
                Otp.valid=False
                Otp.save()
            # print(marks)
            return JsonResponse({"marks":round(marks,2)},status=200)
            # return round(marks,2)
            
        except Quiz.DoesNotExist:
            return JsonResponse({"error":"error"},status=200) 
    return JsonResponse({"reject_message":"You are not Allowed to Access This Exam,Please Validate Your Code"},status=200)    
# @login_required(login_url='/account/')
def GetAllAnswer(request):
    # #
    # id="909b80c2-7e31-4be6-b53b-01000d23ea2f"
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        id=request.GET.get('quiz_id')
        code=request.GET.get('otp')
        print('Ajax request')
        quiz = get_object_or_404(Quiz, id=id)
        code=get_object_or_404(OTP,otp=code)
        quiz_questions = quiz.get_quiz_questions()
        user_answers=UserSubmission.objects.filter(code=code,quiz=quiz)
        print(user_answers)
        print(id)
        context = {"quiz_questions": quiz_questions,"quiz_name":quiz.name}
        html = render_to_string('partial_answer.html', {"quiz_questions":quiz_questions,"quiz_name":quiz.name,"user_answers":user_answers})
        response={
            "html_content": html,
        }
        print("response")
        return JsonResponse(response)
    else:    
        return render(request, 'answers.html') 
        
from django.middleware.csrf import get_token

def get_csrf_token(request):
    # Get the CSRF token using Django's get_token() function
    csrf_token = get_token(request)
    
    # Return the CSRF token in a JSON response
    return JsonResponse({'token': csrf_token})


