from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_board.models import TaskType, Position, Worker, Team, TeamWorker, Tag, Project, Task


admin.site.register(Tag)
admin.site.register(TaskType)
admin.site.register(Position)
