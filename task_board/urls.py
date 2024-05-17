from django.urls import path

from task_board.views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TeamListView,
    TeamDetailView,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("project/create/", ProjectCreateView.as_view(), name="project-create"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("project/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),

    path("project/<int:pk>/task/create", TaskCreateView.as_view(), name="task-create"),
    path("project/<int:pk>/task/<int:task_pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("project/<int:pk>/task/<int:task_pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("project/<int:pk>/task/<int:task_pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    path("teams/", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
]

app_name = "task_board"
