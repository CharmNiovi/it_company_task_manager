from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class UserInTeamRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.team_workers.filter(team__projects__pk=kwargs['pk']).exists():
            raise Http404("You are not authorized to view this page")
        return super().dispatch(request, *args, **kwargs)


class UserTeamOwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.team_workers.filter(team_owner=True, team__projects__pk=kwargs['pk']).exists():
            raise Http404("You are not authorized to view this page")
        return super().dispatch(request, *args, **kwargs)


class TeamStaffOrOwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.team_workers.filter(Q(team_staff=True) | Q(team_owner=True), team__projects__pk=kwargs['pk']).exists():
            raise Http404("You are not authorized to view this page")
        return super().dispatch(request, *args, **kwargs)
