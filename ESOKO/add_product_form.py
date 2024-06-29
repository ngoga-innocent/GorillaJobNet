# forms.py
from django import forms
from .models import Product,Product_Esoko

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'price', 'description', 'thumbnail', 'location', 'contact']
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3'}),
            'name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3', 'placeholder': 'Enter title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3', 'placeholder': 'Enter Short Description'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3', 'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3', 'placeholder': 'Enter location'}),
            'price': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3', 'placeholder': 'Enter Product Price'}),
            'contact': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200 py-2 px-3', 'placeholder': 'Enter contact information'}),
        }
class AddProductEsokoForm(forms.ModelForm):
    class Meta:
        model = Product_Esoko
        fields = ['title', 'slug', 'category', 'product_price', 'description', 'thumbnail', 'product_location', 'owner_contact']
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select mt-1 block w-[90%] rounded-lg bg-slate-200'}),
            'title': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200', 'placeholder': 'Enter title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200', 'placeholder': 'Enter Short Description'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-[90%] rounded-lg bg-slate-200', 'placeholder': 'Enter description'}),
            'product_location': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200', 'placeholder': 'Enter location'}),
            'owner_contact': forms.TextInput(attrs={'class': 'form-input mt-1 block w-[90%] rounded-lg bg-slate-200', 'placeholder': 'Enter contact information'}),
        }        
