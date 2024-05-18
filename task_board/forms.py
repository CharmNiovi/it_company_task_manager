from django import forms
from django.contrib.auth import get_user_model

from task_board.models import Project, Team, Task


class ProjectForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(team_workers__worker=user, team_workers__team_owner=True)

    class Meta:
        model = Project
        fields = ["name", "team"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "tags", "assignees"]


class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
