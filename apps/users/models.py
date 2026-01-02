from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel

        
class User(AbstractUser, TimeStampedModel):
    """User model"""
    
    phone_number = models.CharField(max_length=15, unique=True)
    avatar = models.CharField(max_length=1024, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    

