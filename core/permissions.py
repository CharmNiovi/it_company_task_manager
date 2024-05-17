from django.db.models import Q
from django.contrib.auth.mixins import AccessMixin


class TeamWorkerBasedAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        filter_methods = self.get_all_filter()
        user = request.user.team_workers

        for method in filter_methods:
            user = getattr(self, method)(user, **kwargs)

        if not user.exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    @classmethod
    def get_all_filter(cls):
        return [method for method in dir(cls) if callable(getattr(cls, method)) and method.startswith("filter_")]


class UserInTeamProjectRequiredMixin(TeamWorkerBasedAccessMixin):
    @staticmethod
    def filter_team_project_pk(user, **kwargs):
        return user.filter(team__projects__pk=kwargs['pk'])


class UserTeamOwnerRequiredMixin(UserInTeamProjectRequiredMixin):
    @staticmethod
    def filter_team_owner(user, **kwargs):
        return user.filter(team_owner=True)


class TeamStaffOrOwnerRequiredMixin(UserInTeamProjectRequiredMixin):
    @staticmethod
    def filter_team_owner_or_staff(user, **kwargs):
        return user.filter(Q(team_owner=True) | Q(team_staff=True))


class UserInTeamTeamRequiredMixin(TeamWorkerBasedAccessMixin):
    @staticmethod
    def filter_team_team_pk(user, **kwargs):
        return user.filter(team__pk=kwargs['pk'])


class UserTeamOwnerTeamRequiredMixin(UserTeamOwnerRequiredMixin, UserInTeamTeamRequiredMixin):
    pass
