from django.contrib import admin
from .models import Company, Job, Application, Notification, SavedJob


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'owner',
    )

    search_fields = (
        'name',
        'location',
        'owner__username',
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company',
        'location',
        'job_type',
        'is_active',
        'deadline',
        'created_at',
    )

    list_filter = (
        'job_type',
        'is_active',
        'location',
    )

    search_fields = (
        'title',
        'company__name',
        'location',
        'skills',
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'job',
        'status',
        'applied_at',
    )

    list_filter = (
        'status',
        'applied_at',
    )

    search_fields = (
        'student__username',
        'student__email',
        'job__title',
    )

    list_editable = (
        'status',
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'user__username',
        'message',
    )


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'job',
        'saved_at',
    )

    search_fields = (
        'student__username',
        'student__email',
        'job__title',
    )

    list_filter = (
        'saved_at',
    )