from django.contrib.auth.mixins import AccessMixin
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
        return [
            method
            for method in dir(cls)
            if callable(getattr(cls, method)) and method.startswith("filter_")
        ]
