from core.permissions import TeamWorkerBasedAccessMixin

from django.contrib.auth import get_user_model


class RequestedUserInSameTeamRequiredMixin(TeamWorkerBasedAccessMixin):
    """
    Mixin class that checks if the requested user is in the same team as the profile user.
    """

    def filter_team_project_pk(self, user, *args, **kwargs):
        if self.request.user.username != kwargs["username"]:
            return user.filter(team__worker__username=kwargs["username"])
        return get_user_model().objects.filter(username=self.request.user.username)
