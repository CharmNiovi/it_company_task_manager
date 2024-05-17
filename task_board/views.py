from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from core.permissions import UserTeamOwnerRequiredMixin, TeamStaffOrOwnerRequiredMixin, UserInTeamRequiredMixin
from task_board.forms import ProjectForm, TaskForm
from task_board.models import Project, Task, TeamWorker, Team


class ProjectListView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        return Project.objects.filter(team__worker=self.request.user).select_related("team")

