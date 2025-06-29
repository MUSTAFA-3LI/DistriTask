from django.db import models
from users.models import User
from django.utils.timezone import now


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'delayed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employee'},related_name='assigned_tasks')  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')  
    created_at = models.DateTimeField(auto_now_add=True) #auto set local time
    deadline = models.DateTimeField(default=now)  # ✅ Set default to current time
    category = models.CharField(max_length=100, blank=False, null=False) #will used on distribute tasks on users
    deadline_reached = models.BooleanField(default=False)  # for celery to check task status

    

def __str__(self):
    return f"{self.title} - {self.get_priority_display()}"
