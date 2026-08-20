from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    college = models.CharField(max_length=150, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)

    def __str__(self):
        return self.user.username