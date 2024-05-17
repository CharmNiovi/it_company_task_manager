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


class ProjectUpdateView(UserTeamOwnerRequiredMixin, generic.UpdateView):
    model = Project
    fields = ('name',)

    def get_success_url(self):
        return reverse('task_board:project-detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(UserTeamOwnerRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('task_board:project-list')


class TaskCreateView(TeamStaffOrOwnerRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_board/project_form.html'

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('task_board:project-detail', kwargs={'pk': self.object.project.pk})


class TaskDetailView(UserInTeamRequiredMixin, generic.DetailView):
    def get_object(self, queryset=None):
        return get_object_or_404(Task, project__pk=self.kwargs['pk'], pk=self.kwargs['task_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_worker = TeamWorker.objects.get(team__projects__pk=self.kwargs['pk'], worker=self.request.user)
        context["is_owner"] = team_worker.team_owner
        context["is_staff"] = team_worker.team_staff
        return context


class TaskUpdateView(TeamStaffOrOwnerRequiredMixin, generic.UpdateView):
    model = Task
    fields = ('name', 'description', 'deadline', 'priority', 'task_type', 'tags', "is_completed")
    template_name = 'task_board/project_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, project__pk=self.kwargs['pk'], pk=self.kwargs['task_pk'])

    def get_success_url(self):
        return reverse('task_board:project-detail', kwargs={'pk': self.object.project.pk})


class TaskDeleteView(TeamStaffOrOwnerRequiredMixin, generic.DeleteView):
    model = Task
    template_name = 'task_board/project_confirm_delete.html'

    def get_success_url(self):
        return reverse('task_board:project-detail', kwargs={'pk': self.object.project.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(Task, project__pk=self.kwargs['pk'], pk=self.kwargs['task_pk'])
