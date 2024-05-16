from django import forms

from task_board.models import Project, Team, Task


class ProjectForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(team_workers__worker=user, team_workers__team_owner=True)

    class Meta:
        model = Project
        fields = ["name", "team"]
