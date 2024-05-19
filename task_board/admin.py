from django.contrib import admin

from task_board.models import Project, Tag, Task, TaskType, Team, TeamWorker


admin.site.register(Tag)
admin.site.register(TaskType)


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


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General info", {"fields": ("name", "description")}),
        ("Tags", {"fields": ("tags",)}),
        ("Time info", {"fields": ("priority", "deadline", "is_completed")}),
        ("Specific info", {"fields": ("task_type", "project", "status", "assignees")}),
    )
    list_display = ("name", "deadline", "is_completed", "priority", "task_type", "project")
    search_fields = ("name", "priority", "task_type")
    list_filter = ("priority", "is_completed")
