from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Task(models.Model):
    STATUS_TO_DO = 'Todo'
    STATUS_IN_PROGRESS = 'Inprogress'
    STATUS_DONE = 'Done'

    STATUS_CHOICES = [
        (STATUS_TO_DO,'To do'),
        (STATUS_IN_PROGRESS,'In progress'),
        (STATUS_DONE,'Done'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    sequence = models.IntegerField()
    status = models.CharField(max_length=255, choices= STATUS_CHOICES, default= STATUS_TO_DO)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    last_updated = models.DateTimeField()
    
