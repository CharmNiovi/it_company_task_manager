import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from .models import Project, Team, TeamWorker, Task


class ProjectListViewTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        team = Team.objects.create(name='Test Team')
        TeamWorker.objects.create(team=team, worker=user, team_owner=True)
        Project.objects.create(name='Test Project 1', team=team)
        Project.objects.create(name='Test Project 2', team=team)

    def test_get_unlogged(self):
        request = self.client.get(reverse("task_board:project-list"))
        self.assertEqual(request.status_code, 302)

    def test_get_logged(self):
        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse("task_board:project-list"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.context_data["object_list"].count(), 2)


class ProjectDetailViewTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.team = Team.objects.create(name="testteam")
        self.team_worker = TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)
        self.project = Project.objects.create(name="testproject", team=self.team)

    def test_get_queryset_not_logged_in(self):
        response = self.client.get(reverse("task_board:project-detail", kwargs={"pk": self.project.pk}))
        self.assertEqual(response.status_code, 302)

    def test_get_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("task_board:project-detail", kwargs={"pk": self.project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object"], self.project)
        self.assertEqual(response.context_data["is_owner"], True)
        self.assertEqual(response.context_data["is_staff"], False)


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



class ProjectUpdateViewTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_project_update_view_get_not_owner(self):
        team = Team.objects.create(name="testteam")
        TeamWorker.objects.create(team=team, worker=self.user)
        project = Project.objects.create(name="testproject", team=team)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:project-update', kwargs={'pk': project.pk}))

        self.assertEqual(request.status_code, 404)

    def test_project_update_view_get_not_in_team(self):
        team = Team.objects.create(name="testteam")
        user2 = get_user_model().objects.create_user(username='testuser1', password='testpassword')
        TeamWorker.objects.create(team=team, worker=user2)
        project = Project.objects.create(name="testproject", team=team)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:project-update', kwargs={'pk': project.pk}))

        self.assertEqual(request.status_code, 404)

    def test_project_update_view_post(self):
        data = {'name': 'Updated Project'}
        team = Team.objects.create(name="testteam")
        TeamWorker.objects.create(team=team, worker=self.user, team_owner=True)
        project = Project.objects.create(name="testproject", team=team)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.post(reverse('task_board:project-update', kwargs={'pk': project.pk}), data, follow=True)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(Project.objects.first().name, data["name"])


class ProjectDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.team = Team.objects.create(name="testteam")
        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)
        self.project = Project.objects.create(name="testproject", team=self.team)

    def test_project_delete_view_get_not_owner(self):
        self.client.login(username="testuser", password="testpassword")
        user2 = get_user_model().objects.create_user(username='testuser2', password='testpassword')
        self.client.force_login(user2)
        response = self.client.get(reverse('task_board:project-delete', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 404)

    def test_project_delete_view_get_not_in_team(self):
        self.client.login(username="testuser", password="testpassword")
        user2 = get_user_model().objects.create_user(username='testuser2', password='testpassword')
        TeamWorker.objects.create(team=self.team, worker=user2)
        self.client.force_login(user2)
        response = self.client.get(reverse('task_board:project-delete', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 404)

    def test_project_delete_view_post(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('task_board:project-delete', kwargs={'pk': self.project.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 0)


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.team = Team.objects.create(name="testteam")
        self.project = Project.objects.create(name="testproject", team=self.team)

    def test_get_not_in_team(self):
        user2 = get_user_model().objects.create_user(username='testuser1', password='testpassword')
        TeamWorker.objects.create(team=self.team, worker=user2)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-create', kwargs={'pk': self.project.pk}))

        self.assertEqual(request.status_code, 404)

    def test_get_without_status(self):
        TeamWorker.objects.create(team=self.team, worker=self.user)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-create', kwargs={'pk': self.project.pk}))

        self.assertEqual(request.status_code, 404)

    def test_get_with_owner_status(self):
        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-create', kwargs={'pk': self.project.pk}))
        self.assertEqual(request.status_code, 200)

    def test_get_with_staff_status(self):
        TeamWorker.objects.create(team=self.team, worker=self.user, team_staff=True)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-create', kwargs={'pk': self.project.pk}))
        self.assertEqual(request.status_code, 200)

    def test_form_valid(self):
        data = {
            'name': 'Test Task',
            'description': 'Test Description',
            'deadline': datetime.datetime(2022, 2, 1),
            'priority': 'L',
        }

        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.post(reverse('task_board:task-create', kwargs={'pk': self.project.pk}), data, follow=True)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().status, "UA")


class TaskDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.team = Team.objects.create(name="testteam")
        self.project = Project.objects.create(name="testproject", team=self.team)

    def test_get_not_in_team(self):
        user2 = get_user_model().objects.create_user(username='testuser1', password='testpassword')
        TeamWorker.objects.create(team=self.team, worker=user2)
        task = Task.objects.create(name="testtask", project=self.project, description='Test Description', deadline=datetime.datetime(2022, 2, 1), priority='L')

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-detail', kwargs={'pk': self.project.pk, "task_pk": task.pk}))

        self.assertEqual(request.status_code, 404)

    def test_get(self):
        TeamWorker.objects.create(team=self.team, worker=self.user)
        task = Task.objects.create(name="testtask", project=self.project, description='Test Description',
                                   deadline=datetime.datetime(2022, 2, 1), priority='L')

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-detail', kwargs={'pk': self.project.pk, "task_pk": task.pk}))

        self.assertEqual(request.status_code, 200)


class TaskUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.team = Team.objects.create(name='TestTeam')
        self.project = Project.objects.create(name='TestProject', team=self.team)
        self.task = Task.objects.create(name="testtask", project=self.project, description='Test Description', deadline=datetime.datetime(2022, 2, 1), priority='L')

    def test_get_not_in_team(self):
        user2 = get_user_model().objects.create_user(username='testuser1', password='testpassword')
        TeamWorker.objects.create(team=self.team, worker=user2)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-update', kwargs={'pk': self.project.pk, 'task_pk': self.task.pk}))

        self.assertEqual(request.status_code, 404)

    def test_get_without_status(self):
        user2 = get_user_model().objects.create_user(username='testuser1', password='testpassword')
        TeamWorker.objects.create(team=self.team, worker=user2)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-update', kwargs={'pk': self.project.pk, 'task_pk': self.task.pk}))

        self.assertEqual(request.status_code, 404)

    def test_get_with_owner_status(self):
        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-update', kwargs={'pk': self.project.pk, 'task_pk': self.task.pk}))
        self.assertEqual(request.status_code, 200)

    def test_get_with_staff_status(self):
        TeamWorker.objects.create(team=self.team, worker=self.user, team_staff=True)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.get(reverse('task_board:task-update', kwargs={'pk': self.project.pk, 'task_pk': self.task.pk}))
        self.assertEqual(request.status_code, 200)

    def test_post(self):
        data = {
            'name': 'New Task Name',
            'description': 'New Task Description',
            "project": self.project.pk,
            "deadline": "2022-02-01",
            "priority": "L",
            "status": "UA"
        }

        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)

        self.client.login(username="testuser", password="testpassword")
        request = self.client.post(reverse("task_board:task-update", kwargs={'pk': self.project.pk, 'task_pk': self.task.pk}), data, follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(Task.objects.get(pk=self.task.pk).name, 'New Task Name')
