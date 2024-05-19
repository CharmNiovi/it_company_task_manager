from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from .models import Project, Team, TeamWorker
from .views import ProjectListView


class ProjectListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        team = Team.objects.create(name='Test Team')
        TeamWorker.objects.create(team=team, worker=user, team_owner=True)
        Project.objects.create(name='Test Project 1', team=team)
        Project.objects.create(name='Test Project 2', team=team)

    def setUp(self):
        self.user = get_user_model().objects.get(username='testuser')

    def test_get_unlogged(self):
        request = self.client.get(reverse("task_board:project-list"))
        self.assertEqual(request.status_code, 302)

    def test_get_logged(self):
        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse("task_board:project-list"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.context_data["object_list"].count(), 2)
