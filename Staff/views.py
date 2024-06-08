from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from Quiz.models import Quiz,Faculties,Question,Answer
import json
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# Create your views here.

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url=reverse_lazy('login'))
def Home(request):
    
        return render(request,'staff_homepage.html')
    
class Exam(View):
    @method_decorator(staff_member_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self,request):
        exams=Quiz.objects.all()
        context={"exams":exams}
        return render(request,'staff_exam.html',context) 
   
    def post(self,request):
        name = request.POST.get('name')
        faculty_id = request.POST.get('faculity')
        
        duration = request.POST.get('duration')
        
        passing_marks = request.POST.get('passing_marks')

        try:
            faculty = Faculties.objects.get(id=faculty_id)
            exam = Quiz.objects.create(
                name=name,
                faculty=faculty,
                # description=description,
                time=duration,
                # number_of_questions=number_of_questions,
                required_score_to_pass=passing_marks
            )
            if exam:
             return JsonResponse({'status': True, 'exam_id': exam.id},status=200)
            else:
                 return JsonResponse({'status': False, 'message': "failed to save the exam try again"},status=200)
        except Faculties.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Faculity does not exist'}, status=200)
class Faculity(View):
     def get(self,request):
          faculities=Faculties.objects.all()
          return render(request,'faculities.html',{'faculities':faculities})
             
def DeleteQuestion(request):
        pass
def DeleteExam(request):
        pass        
        
class QuestionView(View):
    
    def post(self,request):
        exam=request.POST.get('exam_id')
        data=json.loads(request.POST.get('data'))
        
        answers=data.get('options')
        question=data.get('question_text')
        try:
            quiz=Quiz.objects.get(id=exam)
            question=Question.objects.create(text=question,quiz=quiz) 
            for answer in answers:
                text=answer.get('text')
                correct=answer.get('correct')
                answer=Answer.objects.create(text=text,correct=correct,question=question)
            return JsonResponse({"status": "success", "message": "Saved"},status=200)    
        except Quiz.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Quiz does not exist'}, status=200)        

        # return JsonResponse({'status': 'saved form'},status=200)
   
    def get(self,request):
        return render(request,'add_question.html')        
        
        
def get_All_faculty(request):
    faculities=Faculties.objects.all().values('id','name')
    items_list = list(faculities)  # Convert QuerySet to a list
    return JsonResponse(items_list, safe=False)

def get_Quiz(request):
    quiz_id = request.GET.get('exam_id')
    try:
        quiz=Quiz.objects.get(id=quiz_id)
        return JsonResponse({"exam": {
            "name":quiz.name,
        },"status":"success"},status=200)
    except Quiz.DoesNotExist:
        return JsonResponse({"status":False,"message": "Quiz not Found"}, status=200)

def get_quiz_questions(request):
    
        exam_id = request.GET.get('exam_id')
        try:
            exam = Quiz.objects.get(id=exam_id)
            questions = Question.objects.filter(quiz=exam)
            
            # Serialize questions and include associated answers
            questions_data = []
            for question in questions:
                qustion_answers= Answer.objects.filter(question=question)
                questions_data.append({
                    # 'id': question.id,
                    'text': question.text,
                    'options': [{'text': answer.text, 'correct': answer.correct} for answer in qustion_answers]
                })
            print(questions_data)       
            
            return JsonResponse({'status': True, 'questions': questions_data})
        except Quiz.DoesNotExist:
            return JsonResponse({"status": False, "message": "Quiz not found"}, status=404)
