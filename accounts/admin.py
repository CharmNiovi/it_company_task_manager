from accounts.models import Position, Worker

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]["fields"] += ("position", "profile_picture")
    list_filter = UserAdmin.list_filter + ("position",)
