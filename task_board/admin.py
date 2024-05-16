from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_board.models import TaskType, Position, Worker, Team, TeamWorker, Tag, Project, Task


admin.site.register(Tag)
admin.site.register(TaskType)
admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] += ('position',)
    list_filter = UserAdmin.list_filter + ("position",)


class TeamWorkerInline(admin.TabularInline):
    model = TeamWorker
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    fieldsets = (
        ("Team name", {"fields": ("name", )}),
    )
    inlines = (TeamWorkerInline,)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team")
    search_fields = ("name", "team__name")
    fieldsets = (
        ("Info", {"fields": ("name", "team")}),
    )
