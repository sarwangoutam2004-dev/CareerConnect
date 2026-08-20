
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, Notification, Company, SavedJob
from django.utils import timezone
from django.db import models


def home(request):
    return render(request, 'home.html')


def job_list(request):

    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')

    today = timezone.localdate()

    jobs = Job.objects.filter(
        is_active=True
    ).filter(
        deadline__isnull=True
    ) | Job.objects.filter(
        is_active=True,
        deadline__gte=today
    )

    jobs = jobs.order_by('-created_at')

    if query:
        jobs = jobs.filter(
            title__icontains=query
        ) | jobs.filter(
            skills__icontains=query
        ) | jobs.filter(
            company__name__icontains=query
        ) | jobs.filter(
            description__icontains=query
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if job_type:
        jobs = jobs.filter(
            job_type=job_type
        )

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query,
        'location': location,
        'job_type': job_type,
        'today': today,
    })


@login_required
def job_detail(request, job_id):

    # Recruiter should not use student job detail
    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    job = get_object_or_404(
        Job,
        id=job_id
    )

    already_applied = Application.objects.filter(
        student=request.user,
        job=job
    ).exists()

    is_saved = SavedJob.objects.filter(
        student=request.user,
        job=job
    ).exists()

    return render(
        request,
        'jobs/job_detail.html',
        {
            'job': job,
            'already_applied': already_applied,
            'is_saved': is_saved,
            'today': timezone.localdate(),
        }
    )


@login_required
def apply_job(request, job_id):

    # Recruiter cannot apply for jobs
    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Check if job is closed
    if not job.is_active:
        return redirect('job_detail', job_id=job.id)

    # Check deadline
    if job.deadline and job.deadline < timezone.localdate():
        return redirect('job_detail', job_id=job.id)

    # Check if already applied
    already_applied = Application.objects.filter(
        student=request.user,
        job=job
    ).exists()

    if already_applied:
        return redirect('job_detail', job_id=job.id)

    # Create application
    application = Application.objects.create(
        student=request.user,
        job=job
    )

    # Notify recruiter
    Notification.objects.create(
        user=job.company.owner,
        message=(
            f"{request.user.username} has applied for your job "
            f"'{job.title}'."
        )
    )

    return redirect('my_applications')
@login_required
def my_applications(request):

    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    applications = Application.objects.filter(
        student=request.user
    ).select_related(
        'job',
        'job__company'
    )

    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })


@login_required
def withdraw_application(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id,
        student=request.user
    )

    application.delete()

    return redirect('my_applications')


@login_required
def recruiter_dashboard(request):

    # Only recruiter/company owner can access
    if not Company.objects.filter(owner=request.user).exists():
        return redirect('dashboard')

    jobs = Job.objects.filter(
        company__owner=request.user
    ).order_by('-created_at')

    total_jobs = jobs.count()

    total_applicants = Application.objects.filter(
        job__in=jobs
    ).count()

    shortlisted = Application.objects.filter(
        job__in=jobs,
        status='Shortlisted'
    ).count()

    rejected = Application.objects.filter(
        job__in=jobs,
        status='Rejected'
    ).count()

    pending = Application.objects.filter(
        job__in=jobs,
        status='Applied'
    ).count()

    active_jobs = jobs.filter(is_active=True).count()

    closed_jobs = jobs.filter(is_active=False).count()

    return render(request, 'jobs/recruiter_dashboard.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'pending': pending,
        'active_jobs': active_jobs,
        'closed_jobs': closed_jobs,
        'today': timezone.localdate(),
    })


@login_required
def create_job(request):

    if not Company.objects.filter(owner=request.user).exists():
        return redirect('dashboard')

    companies = request.user.companies.all()

    if not companies.exists():
        return render(request, 'jobs/create_job.html', {
            'error': 'No company is assigned to your account.'
        })

    company = companies.first()

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        job_type = request.POST.get('job_type')
        skills = request.POST.get('skills')
        deadline = request.POST.get('deadline')

        Job.objects.create(
            company=company,
            title=title,
            description=description,
            location=location,
            salary=salary,
            job_type=job_type,
            skills=skills,
            deadline=deadline
        )

        return redirect('recruiter_dashboard')

    return render(request, 'jobs/create_job.html')


@login_required
def edit_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        company__owner=request.user
    )

    if request.method == 'POST':

        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')
        job.job_type = request.POST.get('job_type')
        job.skills = request.POST.get('skills')
        job.deadline = request.POST.get('deadline')

        job.save()

        return redirect('recruiter_dashboard')

    return render(request, 'jobs/edit_job.html', {
        'job': job
    })


@login_required
def delete_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        company__owner=request.user
    )

    if request.method == 'POST':

        job.delete()

        return redirect('recruiter_dashboard')

    return render(request, 'jobs/delete_job.html', {
        'job': job
    })


@login_required
def close_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        company__owner=request.user
    )

    job.is_active = False
    job.save()

    return redirect('recruiter_dashboard')


@login_required
def reopen_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        company__owner=request.user
    )

    job.is_active = True
    job.save()

    return redirect('recruiter_dashboard')

@login_required
def job_applicants(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        company__owner=request.user
    )

    applications = Application.objects.filter(
        job=job
    ).select_related(
        'student'
    ).order_by(
        models.Case(
            models.When(status='Applied', then=0),
            models.When(status='Shortlisted', then=1),
            models.When(status='Rejected', then=2),
            default=3,
            output_field=models.IntegerField(),
        ),
        '-applied_at'
    )

    return render(request, 'jobs/job_applicants.html', {
        'job': job,
        'applications': applications,
    })

@login_required
def shortlist_application(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company__owner=request.user
    )

    application.status = 'Shortlisted'
    application.save()

    # Notification goes ONLY to the student
    Notification.objects.create(
        user=application.student,
        message=(
            f"Your application for {application.job.title} "
            f"has been shortlisted!"
        )
    )

    return redirect(
        'job_applicants',
        job_id=application.job.id
    )


@login_required
def reject_application(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company__owner=request.user
    )

    application.status = 'Rejected'
    application.save()

    # Notification goes ONLY to the student
    Notification.objects.create(
        user=application.student,
        message=(
            f"Your application for {application.job.title} "
            f"has been rejected."
        )
    )

    return redirect(
        'job_applicants',
        job_id=application.job.id
    )


@login_required
def update_application_status(request, application_id, status):

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company__owner=request.user
    )

    if status in ['Shortlisted', 'Rejected']:

        application.status = status
        application.save()

        if status == 'Shortlisted':
            message = (
                f"Your application for {application.job.title} "
                f"has been shortlisted!"
            )
        else:
            message = (
                f"Your application for {application.job.title} "
                f"has been rejected."
            )

        Notification.objects.create(
            user=application.student,
            message=message
        )

    return redirect(
        'job_applicants',
        job_id=application.job.id
    )


@login_required
def notifications(request):

    notification_list = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    notification_list.update(is_read=True)

    return render(request, 'jobs/notifications.html', {
        'notifications': notification_list
    })


# ==========================================
# COMPANY PROFILE
# ==========================================

@login_required
def company_profile(request):

    company = get_object_or_404(
        Company,
        owner=request.user
    )

    if request.method == 'POST':

        company.name = request.POST.get('name')
        company.website = request.POST.get('website')
        company.location = request.POST.get('location')

        company.save()

        return redirect('company_profile')

    return render(request, 'jobs/company_profile.html', {
        'company': company
    })


@login_required
def save_job(request, job_id):

    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.get_or_create(
        student=request.user,
        job=job
    )

    return redirect('job_detail', job_id=job.id)


@login_required
def remove_saved_job(request, job_id):

    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.filter(
        student=request.user,
        job=job
    ).delete()

    return redirect('job_detail', job_id=job.id)


@login_required
def saved_jobs(request):

    if Company.objects.filter(owner=request.user).exists():
        return redirect('recruiter_dashboard')

    saved_jobs = SavedJob.objects.filter(
        student=request.user
    ).select_related(
        'job',
        'job__company'
    ).order_by('-saved_at')

    return render(request, 'jobs/saved.html', {
        'saved_jobs': saved_jobs
    })

