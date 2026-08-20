from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.job_list,
        name='job_list'
    ),

    path(
        'applications/',
        views.my_applications,
        name='my_applications'
    ),
    path(
    'applications/<int:application_id>/withdraw/',
    views.withdraw_application,
    name='withdraw_application'
    ),

    path(
        'recruiter/',
        views.recruiter_dashboard,
        name='recruiter_dashboard'
    ),
    path(
    '<int:job_id>/applicants/',
    views.job_applicants,
    name='job_applicants'
),

    path(
        '<int:job_id>/apply/',
        views.apply_job,
        name='apply_job'
    ),

    path(
        '<int:job_id>/',
        views.job_detail,
        name='job_detail'
    ),
    path(
    '<int:application_id>/shortlist/',
    views.shortlist_application,
    name='shortlist_application'
),

path(
    '<int:application_id>/reject/',
    views.reject_application,
    name='reject_application'
),
path(
    'recruiter/create-job/',
    views.create_job,
    name='create_job'
),
path(
    'recruiter/job/<int:job_id>/edit/',
    views.edit_job,
    name='edit_job'
),

path(
    'recruiter/job/<int:job_id>/delete/',
    views.delete_job,
    name='delete_job'
),
path(
    'recruiter/application/<int:application_id>/<str:status>/',
    views.update_application_status,
    name='update_application_status'
),
path(
    'notifications/',
    views.notifications,
    name='notifications'
),
path(
    'recruiter/company/',
    views.company_profile,
    name='company_profile'
),
path(
    'recruiter/job/<int:job_id>/close/',
    views.close_job,
    name='close_job'
),

path(
    'recruiter/job/<int:job_id>/reopen/',
    views.reopen_job,
    name='reopen_job'
),
path(
    'job/<int:job_id>/save/',
    views.save_job,
    name='save_job'
),

path(
    'job/<int:job_id>/remove-save/',
    views.remove_saved_job,
    name='remove_saved_job'
),

path(
    'saved-jobs/',
    views.saved_jobs,
    name='saved_jobs'
),


]