from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class UserInTeamRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.check_authorization(request, **kwargs):
            raise Http404("You are not authorized to view this page")
        return super().dispatch(request, *args, **kwargs)

    def check_authorization(self, request, **kwargs):
        if request.user.is_anonymous:
            return False
        return request.user.team_workers.filter(
                team__projects__pk=kwargs['pk']
        ).exists()


class UserTeamOwnerRequiredMixin(UserInTeamRequiredMixin):
    def check_authorization(self, request, **kwargs):
        if request.user.is_anonymous:
            return False
        return request.user.team_workers.filter(team_owner=True).exists()


class UserTeamStaffRequiredMixin(UserInTeamRequiredMixin):
    def check_authorization(self, request, **kwargs):
        if request.user.is_anonymous:
            return False
        return request.user.team_workers.filter(team_staff=True).exists()
