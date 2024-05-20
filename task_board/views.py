from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from task_board.forms import ProjectForm, TaskForm, TeamUpdateForm
from task_board.models import Project, Task, Team, TeamWorker
from task_board.permissions import (
    TeamStaffOrOwnerRequiredMixin,
    UserInTeamProjectRequiredMixin,
    UserInTeamTeamRequiredMixin,
    UserTeamOwnerProjectRequiredMixin,
    UserTeamOwnerTeamRequiredMixin
)


class ProjectListView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        return Project.objects.filter(team__worker=self.request.user).select_related("team")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    def get_queryset(self):
        return Project.objects.filter(
            team__worker=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_worker = TeamWorker.objects.get(
            team__projects__pk=self.kwargs["pk"],
            worker=self.request.user
        )
        context["is_owner"] = team_worker.team_owner
        context["is_staff"] = team_worker.team_staff
        context["tasks"] = context["object"].tasks.order_by(
            "deadline", "-priority"
        ).select_related(
            "task_type"
        ).prefetch_related(
            "tags", "assignees"
        )
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ProjectForm
    template_name = "task_board/project_form.html"

    def get_success_url(self):
        return reverse("task_board:project-detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProjectUpdateView(LoginRequiredMixin,
                        UserTeamOwnerProjectRequiredMixin,
                        generic.UpdateView):
    model = Project
    fields = ("name",)

    def get_success_url(self):
        return reverse("task_board:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin,
                        UserTeamOwnerProjectRequiredMixin,
                        generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task_board:project-list")


class TaskCreateView(LoginRequiredMixin, TeamStaffOrOwnerRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_board/task_form.html"

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs["pk"])
        form.instance.status = "IP" if form.cleaned_data.get("assignees") else "UA"
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("task_board:project-detail", kwargs={"pk": self.object.project.pk})


class TaskDetailView(LoginRequiredMixin, UserInTeamProjectRequiredMixin, generic.DetailView):
    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            project__pk=self.kwargs["pk"],
            pk=self.kwargs["task_pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_worker = TeamWorker.objects.get(
            team__projects__pk=self.kwargs["pk"],
            worker=self.request.user
        )
        context["is_owner"] = team_worker.team_owner
        context["is_staff"] = team_worker.team_staff
        return context


class TaskUpdateView(LoginRequiredMixin, TeamStaffOrOwnerRequiredMixin, generic.UpdateView):
    model = Task
    fields = (
        "name",
        "description",
        "deadline",
        "priority",
        "task_type",
        "tags",
        "status",
        "assignees"
    )
    template_name = "task_board/task_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            project__pk=self.kwargs["pk"],
            pk=self.kwargs["task_pk"]
        )

    def get_success_url(self):
        return reverse("task_board:project-detail", kwargs={"pk": self.object.project.pk})


class TaskDeleteView(LoginRequiredMixin, TeamStaffOrOwnerRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_board/task_confirm_delete.html"

    def get_success_url(self):
        return reverse("task_board:project-detail", kwargs={"pk": self.object.project.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            project__pk=self.kwargs["pk"],
            pk=self.kwargs["task_pk"]
        )


class TeamListView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        return Team.objects.filter(
            team_workers__worker=self.request.user
        ).values(
            "pk", "name", "team_workers__team_owner", "team_workers__team_staff"
        )


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = ("name", )
    template_name = "task_board/team_form.html"

    def get_success_url(self):
        return reverse("task_board:team-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        TeamWorker.objects.create(
            team=self.object,
            worker=self.request.user,
            team_owner=True
        )
        return response


class TeamDetailView(LoginRequiredMixin, UserInTeamTeamRequiredMixin, generic.DetailView):
    template_name = "task_board/team_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Team, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_workers"] = TeamWorker.objects.filter(
            team=context["object"]
        ).select_related("worker", "worker__position")
        context["is_owner"] = context["team_workers"].get(
            team=context["object"],
            worker=self.request.user
        ).team_owner
        return context


class AddTeamWorkerInTeamView(LoginRequiredMixin,
                              UserTeamOwnerTeamRequiredMixin,
                              generic.FormView):
    form_class = TeamUpdateForm
    template_name = "task_board/team_form.html"

    def get_success_url(self):
        return reverse("task_board:team-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Team.objects.values("name"), pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        user_to_add = get_object_or_404(get_user_model(), email=form.cleaned_data["email"])
        team = get_object_or_404(Team, pk=self.kwargs["pk"])
        TeamWorker.objects.create(team=team, worker=user_to_add)
        return super(AddTeamWorkerInTeamView, self).form_valid(form)


class ChangeTeamWorkerIsStaffPermissionView(LoginRequiredMixin,
                                            UserTeamOwnerTeamRequiredMixin,
                                            generic.UpdateView):
    model = TeamWorker
    fields = ("team_staff",)
    template_name = "task_board/change_permission_in_team_form.html"

    def get_success_url(self):
        return reverse("task_board:team-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self, queryset=None):
        return get_object_or_404(
            TeamWorker,
            team__pk=self.kwargs["pk"],
            worker__username=self.kwargs["slug"]
        )


class UserDeleteFromTeamView(LoginRequiredMixin,
                             UserTeamOwnerTeamRequiredMixin,
                             generic.DeleteView):
    model = TeamWorker
    template_name = "task_board/team_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            TeamWorker,
            team__pk=self.kwargs["pk"],
            worker__username=self.kwargs["slug"]
        )

    def get_success_url(self):
        return reverse("task_board:team-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.team_owner:
            team_workers = TeamWorker.objects.filter(team=self.object.team)
            if team_workers.exists():
                team_staff = team_workers.filter(team_staff=True)
                if team_staff:
                    team_staff_first = team_staff.first()
                    team_staff_first.team_owner = True
                    team_staff_first.save()
                else:
                    team_workers_first = team_workers.first()
                    team_workers_first.team_owner = True
                    team_workers_first.save()
            else:
                self.object.team.delete()
        return response
