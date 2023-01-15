from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    edited = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(null=True)
