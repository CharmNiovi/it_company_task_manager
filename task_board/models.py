from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    worker = models.ManyToManyField(
        get_user_model(),
        through="TeamWorker",
        related_name="teams"
    )

    def __str__(self):
        return self.name


class TeamWorker(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="team_workers"
    )
    worker = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="team_workers"
    )
    team_owner = models.BooleanField(default=False)
    team_staff = models.BooleanField(default=False)

    def clean(self) -> None:
        if self.team_owner and TeamWorker.objects.filter(
                team=self.team,
                team_owner=True
        ).exclude(worker_id=self.worker_id).exists():
            raise ValidationError("Team owner must be one")

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("team", "worker"), name="unique_worker_in_team"),
        )
        ordering = ("-team_owner", "-team_staff")


class Project(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        UA = ("UA", "Unassigned")
        IP = ("IP", "In Progress")
        IR = ("IR", "In Review")
        D = ("D", "Done")

    class PriorityChoices(models.TextChoices):
        LOW = ("1", "Low Priority")
        MID = ("2", "Mid Priority")
        High = ("3", "High Priority")

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=1, choices=PriorityChoices.choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)
    status = models.CharField(max_length=2, choices=StatusChoices.choices)
    assignees = models.ManyToManyField(get_user_model(), related_name="tasks", blank=True)
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )

    def __str__(self):
        return self.name
