from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from .models import Project, Team, TeamWorker


# class ProjectListViewTestCase(TestCase):
#     def setUp(self):
#         user = get_user_model().objects.create_user(username='testuser', password='testpassword')
#         team = Team.objects.create(name='Test Team')
#         TeamWorker.objects.create(team=team, worker=user, team_owner=True)
#         Project.objects.create(name='Test Project 1', team=team)
#         Project.objects.create(name='Test Project 2', team=team)
#
#     def test_get_unlogged(self):
#         request = self.client.get(reverse("task_board:project-list"))
#         self.assertEqual(request.status_code, 302)
#
#     def test_get_logged(self):
#         self.client.login(username="testuser", password="testpassword")
#         request = self.client.get(reverse("task_board:project-list"))
#         self.assertEqual(request.status_code, 200)
#         self.assertEqual(request.context_data["object_list"].count(), 2)


# class ProjectDetailViewTestCase(TestCase):
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
#         self.team = Team.objects.create(name="testteam")
#         self.team_worker = TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)
#         self.project = Project.objects.create(name="testproject", team=self.team)
#
#     def test_get_queryset_not_logged_in(self):
#         response = self.client.get(reverse("task_board:project-detail", kwargs={"pk": self.project.pk}))
#         self.assertEqual(response.status_code, 302)
#
#     def test_get_logged_in(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.get(reverse("task_board:project-detail", kwargs={"pk": self.project.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context_data["object"], self.project)
#         self.assertEqual(response.context_data["is_owner"], True)
#         self.assertEqual(response.context_data["is_staff"], False)


class ProjectCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username="testuser", password="testpassword")

    def test_get_with_team(self):
        team = Team.objects.create(name="testteam")
        TeamWorker.objects.create(team=team, worker=self.user, team_owner=True)
        response = self.client.get(reverse('task_board:project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['form'].fields["team"].queryset.count(), 1)

    def test_get_without_team(self):
        response = self.client.get(reverse('task_board:project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['form'].fields["team"].queryset.count(), 0)

    def test_post(self):
        team = Team.objects.create(name="testteam")
        TeamWorker.objects.create(team=team, worker=self.user, team_owner=True)
        data = {
            'name': 'testproject',
            'team': team.id,
        }
        response = self.client.post(reverse('task_board:project-create'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, 'testproject')
        self.assertEqual(project.team, team)
