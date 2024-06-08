from django.db import models
import uuid
import random
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from Payment.models import OTP
# Create your models here.
class Faculties(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=255)
    thumbnail=models.ImageField(upload_to='faculty', null=True,default=None)
    description=models.CharField(max_length=255,default='')

    def __str__(self):
        return f"{self.name}"
    
    def get_faculty_quizzes(self):
        return self.quiz_set.all()
    class Meta:
        verbose_name_plural='Faculties'
class Quiz(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=255)
    faculty=models.ForeignKey(Faculties,on_delete=models.CASCADE)
    number_of_questions=models.IntegerField(default=0)
    time=models.IntegerField(default=1,verbose_name='Duration of Quiz')
    required_score_to_pass=models.IntegerField()
    created_at=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name}"
    

    def get_quiz_questions(self):
        question=list(self.question_set.all())
        random.shuffle(question)
        return sorted(question, key=lambda q: q.id)
    def get_user_submissions(self):
        return self.usersubmission_set.all()
    
    class Meta:
        verbose_name_plural ='Quizes' 
class Question(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    text =models.TextField()
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"
    
    def get_question_answer(self):
        return self.answer_set.all()
class Answer(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    text=models.TextField()
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} + {self.correct} + {self.question}" 
class UserSubmission(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    code=models.ForeignKey(OTP, on_delete=models.CASCADE,default='b8287861-aea3-48a3-89b0-8fbd9a8a27cf')
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_response=models.ForeignKey(Answer, on_delete=models.CASCADE,null=True) 
    correct=models.BooleanField(default=False)
    created_on=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"  {self.question.text}  + {self.created_on}"
    # class UserSubmissionsManager(models.Manager):
    
    #     def for_user(self, user):
     
    #         return self.get_queryset().filter(user=user)      

def update_Number_of_Questions(sender,instance,created,**kwargs):
    if created:
        try:
            quiz=Quiz.objects.get(id=instance.quiz.id)
            quiz.number_of_questions = quiz.number_of_questions + 1
            quiz.save()
        except Quiz.DoesNotExist:
            return False
    
       
post_save.connect(update_Number_of_Questions,Question)        