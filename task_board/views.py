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


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    def get_queryset(self):
        return Project.objects.filter(team__worker=self.request.user).prefetch_related("tasks__tags", "tasks__task_type")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_worker = TeamWorker.objects.get(team__projects__pk=self.kwargs['pk'], worker=self.request.user)
        context["is_owner"] = team_worker.team_owner
        context["is_staff"] = team_worker.team_staff
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ProjectForm
    template_name = 'task_board/project_form.html'
    success_url = reverse_lazy('task_board:project-list')

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
