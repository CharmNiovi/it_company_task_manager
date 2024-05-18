from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q


class TeamWorkerBasedAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user.team_workers

        for method in self.get_all_filter():
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


class UserTeamOwnerRequiredMixin(TeamWorkerBasedAccessMixin):
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


class UserTeamOwnerProjectRequiredMixin(UserTeamOwnerRequiredMixin, UserInTeamProjectRequiredMixin):
    pass


class UserTeamOwnerTeamRequiredMixin(UserTeamOwnerRequiredMixin, UserInTeamTeamRequiredMixin):
    pass
