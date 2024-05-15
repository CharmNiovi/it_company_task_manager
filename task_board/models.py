from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)


class Position(models.Model):
    name = models.CharField(max_length=100)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name="workers")


class Team(models.Model):
    name = models.CharField(max_length=50)
    worker = models.ManyToManyField(Worker, related_name="team")


class Project(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        LOW = ("L", "Low Priority")
        MID = ("M", "Mid Priority")
        High = ("H", "High Priority")

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(max_length=1, choices=PriorityChoices.choices)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
