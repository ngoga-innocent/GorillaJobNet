from django.contrib import admin
from .models import Quiz,Faculties,Question,Answer,UserSubmission
# Register your models here.
admin.site.register(Quiz)
admin.site.register(Faculties)


class AnswerInline(admin.TabularInline):
    model = Answer
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline] 

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(UserSubmission)