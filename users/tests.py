import json

from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project
from users.models import Skill, User


class UserRegistrationTests(TestCase):
    def test_register_redirects_to_login(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "name": "Test",
                "surname": "User",
                "email": "test@example.com",
                "password": "securepass123",
            },
        )
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(User.objects.filter(email="test@example.com").exists())


class SkillTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="skill@example.com",
            password="pass12345",
            name="Skill",
            surname="Owner",
            phone="+79001234567",
        )
        self.other = User.objects.create_user(
            email="other@example.com",
            password="pass12345",
            name="Other",
            surname="User",
            phone="+79007654321",
        )
        self.skill = Skill.objects.create(name="Python")
        self.client = Client()

    def test_skills_autocomplete(self):
        response = self.client.get(reverse("users:skills_autocomplete"), {"q": "Py"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Python")

    def test_add_skill_to_profile(self):
        self.client.login(username="skill@example.com", password="pass12345")
        response = self.client.post(
            reverse("users:add_skill", kwargs={"user_id": self.user.pk}),
            data=json.dumps({"skill_id": self.skill.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.skills.filter(pk=self.skill.pk).exists())

    def test_filter_participants_by_skill(self):
        self.user.skills.add(self.skill)
        response = self.client.get(reverse("users:list"), {"skill": "Python"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Skill Owner")
        self.assertNotContains(response, "Other User")


class ProjectTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="pass12345",
            name="Owner",
            surname="User",
            phone="+79001112233",
        )
        self.participant = User.objects.create_user(
            email="member@example.com",
            password="pass12345",
            name="Member",
            surname="User",
            phone="+79004445566",
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Description",
            owner=self.owner,
            status="open",
        )
        self.project.participants.add(self.owner)
        self.client = Client()

    def test_project_list_sorted_newest_first(self):
        from django.utils import timezone
        from datetime import timedelta

        older = Project.objects.create(
            name="Older",
            owner=self.owner,
            status="open",
        )
        Project.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 200)
        projects = list(response.context["page_obj"])
        self.assertEqual(projects[0], self.project)
        self.assertEqual(projects[1], older)

    def test_toggle_participate(self):
        self.client.login(username="member@example.com", password="pass12345")
        url = reverse("projects:toggle_participate", kwargs={"project_id": self.project.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["participant"])
        response = self.client.post(url)
        self.assertFalse(response.json()["participant"])
