from django import forms

from task_board.models import Project, Task, Team


class ProjectForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields["team"].queryset = Team.objects.filter(
            team_workers__worker=user,
            team_workers__team_owner=True
        )

    class Meta:
        model = Project
        fields = ["name", "team"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name", "description", "deadline", "priority", "task_type", "tags", "assignees"
        ]


class TeamUpdateForm(forms.Form):
    email = forms.EmailField()
