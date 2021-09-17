from django.db import models
import os

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    reason_for_use = models.CharField(max_length=64)
    user_type = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.username}: {self.email}"

class Resource(models.Model):
    uploaded_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    upload_date = models.DateField()
    resource_name = models.CharField(max_length=64)
    raw_resource = models.FileField(upload_to='resources/')

    def __str__(self):
        return f"{self.resource_name} by: {self.uploaded_by}"

class QuestionLog(models.Model):
    query = models.TextField()
    answer = models.TextField()
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.query} from {self.resource}"