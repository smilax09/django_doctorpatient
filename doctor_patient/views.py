from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile(user=user,
                              profile_picture=form.cleaned_data['profile_picture'],
                              address_line1=form.cleaned_data['address_line1'],
                              city=form.cleaned_data['city'],
                              state=form.cleaned_data['state'],
                              pincode=form.cleaned_data['pincode'],
                              user_type=form.cleaned_data['user_type'])
            profile.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                profile = Profile.objects.get(user=user)
                if profile.user_type == 'doctor':
                    return redirect('doctor_dashboard')
                elif profile.user_type == 'patient':
                    return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
