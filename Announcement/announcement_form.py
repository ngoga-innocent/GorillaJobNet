# forms.py
from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'category', 'title', 'slug', 'thumbnail', 'description',
            'application_link', 'location','experience','deadline','company_name','announcer_logo', 'announcer_description',
            
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3'}),
            'title': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3', 'placeholder': 'Enter title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3 ', 'placeholder': 'Enter Short Description'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block  '}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-[90%] rounded-lg  bg-slate-200 ', 'placeholder': 'Enter description'}),
            'deadline' : forms.SelectDateWidget(attrs={'class': 'rounded-lg gap-x-1 bg-slate-200 py-2 px-2 mx-1'}),
            'application_link': forms.URLInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3 ', 'placeholder': 'Enter application link'}),
            'announcer': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3', 'placeholder': 'Enter announcer name'}),
            'company_name':forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3', 'placeholder': 'Enter announcer name'}),
            'experience':forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg  bg-slate-200 py-2 px-3', 'placeholder': 'Enter announcer name'}),
            'announcer_description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-[90%] rounded-lg py-2 px-3 bg-slate-200 ', 'placeholder': 'Enter announcer description'}),
            'announcer_logo': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block w-[90%] '}),
            
        }
    def save(self, commit=True, user=None):
        announcement = super().save(commit=False)
        if user is not None:
            announcement.announcer = user
        if commit:
            announcement.save()
        return announcement    
