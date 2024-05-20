from accounts.permissions import RequestedUserInSameTeamRequiredMixin
from django.db.models import Q
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import RegisterForm


class RegisterView(generic.CreateView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("task_board:project-list")

    def form_valid(self, form):
        user = super().form_valid(form)
        login(self.request, self.object)
        return user


class ProfileView(
    LoginRequiredMixin,
    RequestedUserInSameTeamRequiredMixin,
    generic.DetailView
):
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return get_object_or_404(get_user_model(), username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = (
            context["object"].tasks
            .exclude(status="D")
            .order_by("deadline")
            .select_related("project", "task_type")[:10]
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    fields = ("username", "first_name", "last_name", "email", "position", "profile_picture")
    template_name = "registration/worker_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile-detail",
            kwargs={"username": self.object.username}
        )

    def get_object(self, queryset=None):
        return self.request.user
