# clientapp/models.py
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='clients')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User, related_name='assigned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='projects')

    def __str__(self):
        return self.name
