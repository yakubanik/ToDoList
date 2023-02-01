from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    edited = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_todo', kwargs={'todo_id': self.id})
