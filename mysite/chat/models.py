from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Q

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        q = self.get_queryset().filter(lookup).distinct()
        return q

class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()
    class Meta:
        unique_together = ('first_person', 'second_person')


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_message_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)