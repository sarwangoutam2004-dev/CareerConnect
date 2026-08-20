from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='companies'
    )

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Job(models.Model):

    JOB_TYPES = [
        ('Internship', 'Internship'),
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPES
    )

    skills = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title


class Application(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(
        max_length=300
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.message}"


class SavedJob(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_jobs'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'job'],
                name='unique_saved_job'
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"