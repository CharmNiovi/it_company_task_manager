from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class TeamStaffOrOwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.team_workers.filter(
                Q(team_owner=True) | Q(team_staff=True),
                team__projects__pk=kwargs['pk']
        ):
            raise Http404("You are not authorized to view this page")
        return super().dispatch(request, *args, **kwargs)