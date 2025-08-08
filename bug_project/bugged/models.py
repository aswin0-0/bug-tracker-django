from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class bugs_report(models.Model):
    Status_choices=[
        ('cleared','Cleared'),
        ('ongoing','ongoing'),
        ('remained','Remained'),
    ]
    bug_title=models.CharField(max_length=100)
    bug_description=models.TextField()
    status = models.CharField(max_length=10, choices=Status_choices, default='ongoing')



