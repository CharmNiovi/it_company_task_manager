import datetime

from accounts.forms import RegisterForm
from accounts.models import Position

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from task_board.models import Project, Task, Team, TeamWorker


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("accounts:register")

    def test_register_view_get(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertIsInstance(request.context_data["form"], RegisterForm)

    def test_register_view_post(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(get_user_model().objects.filter(username="testuser").count(), 1)
        self.assertTrue(self.client.login(username="testuser", password="testpassword"))


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         password="testpassword",
                                                         email="testuser@example.com")
        self.fried = get_user_model().objects.create_user(username="testuser1",
                                                          password="testpassword1",
                                                          email="testuser1@example.com")
        self.team = Team.objects.create(name="testteam")

    def test_self_profile_view_get(self):
        project = Project.objects.create(name="testproject", team=self.team)
        task1 = Task.objects.create(
            name="testtask",
            deadline=datetime.datetime(2022, 2, 1),
            project=project,
        )
        task2 = Task.objects.create(
            name="testtask1",
            deadline=datetime.datetime(2022, 1, 1),
            project=project,
        )
        task3 = Task.objects.create(
            name="testtask2",
            deadline=datetime.datetime(2022, 2, 1),
            project=project,
            status="D"
        )
        task1.assignees.add(self.user)
        task2.assignees.add(self.user)
        task3.assignees.add(self.user)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse(
            "accounts:profile-detail",
            kwargs={"username": "testuser"}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data["object"], get_user_model())
        self.assertEqual(response.context_data["object"].username, "testuser")
        self.assertEqual(response.context_data["tasks"].count(), 2)
        self.assertEqual(response.context_data["tasks"].values()[0]["name"], "testtask1")

    def test_in_team_profile_view_get(self):
        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)
        TeamWorker.objects.create(team=self.team, worker=self.fried)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse(
            "accounts:profile-detail",
            kwargs={"username": "testuser1"}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object"].username, "testuser1")

    def test_not_in_team_profile_view_get(self):
        TeamWorker.objects.create(team=self.team, worker=self.user, team_owner=True)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse(
            "accounts:profile-detail",
            kwargs={"username": "testuser1"}
        ))

        self.assertEqual(response.status_code, 404)


class ProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         password="testpassword")

    def test_form_valid(self):
        data = {
            "username": "testuser2",
            "first_name": "Updated Test",
            "last_name": "Updated User",
            "email": "updatedtestuser@example.com",
            "position": Position.objects.create(name="Tester").id,
            "profile_picture": "",
        }
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("accounts:profile-update"), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(**data).exists())
