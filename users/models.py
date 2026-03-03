from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model for the chat application.
    Adds is_online and last_seen fields to track user status.
    And email field unique constraint.
    """
    email = models.EmailField(unique=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.username
    
    def mark_online(self):
        self.is_online = True
        self.last_seen = timezone.now()
        self.save(update_fields=['is_online', 'last_seen'])

    def mark_offline(self):
        self.is_online = False
        self.last_seen = timezone.now()
        self.save(update_fields=['is_online', 'last_seen'])
