from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.http import Http404


class TeamWorkerBasedAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user.team_workers

        for method in self.get_all_filter():
            user = getattr(self, method)(user, **kwargs)

        if not user.exists():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    @classmethod
    def get_all_filter(cls):
        return [method for method in dir(cls) if callable(getattr(cls, method)) and method.startswith("filter_")]


class UserInTeamProjectRequiredMixin(TeamWorkerBasedAccessMixin):
    """
    Filter the user based on the team and project primary key.
    """
    @staticmethod
    def filter_team_project_pk(user, **kwargs):
        return user.filter(team__projects__pk=kwargs['pk'])


class UserTeamOwnerRequiredMixin(TeamWorkerBasedAccessMixin):
    """
    Filter the user queryset to only include users who are the owner of the team.
    """
    @staticmethod
    def filter_team_owner(user, **kwargs):
        return user.filter(team_owner=True)


class TeamStaffOrOwnerRequiredMixin(UserInTeamProjectRequiredMixin):
    """
    Filter the user based on the team and project primary key.
    Filter the user queryset to only include users who are either team staff or owners.
    """
    @staticmethod
    def filter_team_owner_or_staff(user, **kwargs):
        return user.filter(Q(team_owner=True) | Q(team_staff=True))


class UserInTeamTeamRequiredMixin(TeamWorkerBasedAccessMixin):
    """
    Filters the user queryset based on the team primary key.
    """
    @staticmethod
    def filter_team_team_pk(user, **kwargs):
        return user.filter(team__pk=kwargs['pk'])


class UserTeamOwnerProjectRequiredMixin(UserTeamOwnerRequiredMixin, UserInTeamProjectRequiredMixin):
    """
    Filter the user queryset to only include users who are the owner of the team.
    Filter the user based on the team and project primary key.
    """
    pass


class UserTeamOwnerTeamRequiredMixin(UserTeamOwnerRequiredMixin, UserInTeamTeamRequiredMixin):
    """
    Filter the user queryset to only include users who are the owner of the team.
    Filters the user queryset based on the team primary key.
    """
    pass
