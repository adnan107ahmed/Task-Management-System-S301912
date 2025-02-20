from django.db import models
from django.contrib.auth.models import AbstractUser

class Project(models.Model):
    name = models.CharField(max_length=160, unique=True)
    def __str__(self):
        return f"Name: {self.name}"

class Task(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6)
    status = models.CharField(max_length=10)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"Title: {self.title}, Description:  {self.description},  Due Date: {self.due_date}, Priority: {self.priority}, Status:  {self.status}"
    
    class User(AbstractUser):
        email = models.EmailField(unique=True)
        phone_number = models.CharField(max_length=15, blank=True,null=True)
        address = models.TextField(blank=True, null=True)

        groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
        user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)

        def __str__(self):
            return self.username
            