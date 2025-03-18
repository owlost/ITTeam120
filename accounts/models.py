from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    user_id = models.AutoField(primary_key=True)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    registration_time = models.DateTimeField(default=now)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
