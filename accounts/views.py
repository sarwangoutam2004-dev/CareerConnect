
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import StudentProfile
from jobs.models import Application, Company


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')


def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


def logout_user(request):

    logout(request)

    return redirect('home')


@login_required
def profile(request):

    # Recruiter ko student profile access nahi dena
    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    student_profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        student_profile.phone = request.POST.get('phone')
        student_profile.college = request.POST.get('college')
        student_profile.degree = request.POST.get('degree')
        student_profile.skills = request.POST.get('skills')

        # Replace Resume
        if request.FILES.get('resume'):

            if student_profile.resume:
                student_profile.resume.delete(save=False)

            student_profile.resume = request.FILES['resume']

        # Delete Resume
        if request.POST.get('delete_resume') == 'yes':

            if student_profile.resume:
                student_profile.resume.delete(save=False)

            student_profile.resume = None

        student_profile.save()

        return redirect('profile')

    return render(request, 'profile.html', {
        'profile': student_profile
    })


@login_required
def dashboard(request):

    # Recruiter ko student dashboard access nahi dena
    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    applications = Application.objects.filter(
        student=request.user
    )

    total_applications = applications.count()

    pending = applications.filter(
        status='Applied'
    ).count()

    shortlisted = applications.filter(
        status='Shortlisted'
    ).count()

    rejected = applications.filter(
        status='Rejected'
    ).count()

    return render(request, 'dashboard.html', {
        'total_applications': total_applications,
        'pending': pending,
        'shortlisted': shortlisted,
        'rejected': rejected,
    })

