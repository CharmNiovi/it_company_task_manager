from django.contrib.auth.models import AbstractUser
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name="workers")


class Team(models.Model):
    name = models.CharField(max_length=50)
    worker = models.ManyToManyField(Worker, through="TeamWorker")


class TeamWorker(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_worker")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="team_worker")
    team_owner = models.BooleanField()
    team_staff = models.BooleanField()

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("team", "team_owner"), name="unique_team_owner"),
        )


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
    tags = models.ManyToManyField(Tag, related_name="tasks")
