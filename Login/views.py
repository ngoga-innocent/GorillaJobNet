from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import random
import string
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))
def signup_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email').strip()

        # Passwords must match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'signup.html')

        # Validate email
        if email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Invalid email address.")
                return render(request, 'signup.html')

        # Optionally add password validation here
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'signup.html')

        # Manually hash the password
        hashed_password = make_password(password)

        # Create the user with the hashed password
        user = User(username=username, email=email, password=hashed_password)
        user.save()

        # Check if the password is being hashed correctly
        if not user.has_usable_password():
            messages.error(request, "Password was not set correctly.Please try again.")
            return render(request, 'signup.html')

        # Attempt to authenticate and log the user in immediately after signup
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Account created successfully and you are now logged in.")
            next_url = request.POST.get('next', reverse_lazy('homepage'))
            return HttpResponseRedirect(next_url)
        else:
            messages.error(request, "There was an issue logging you in. Please try logging in manually.")
            return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            next_url = request.POST.get('next', reverse_lazy('homepage'))
            login(request, user)
            return redirect('homepage')  # or some other page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')
