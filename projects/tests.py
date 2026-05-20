from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project
from users.models import User


class ProjectPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="author@example.com",
            password="pass12345",
            name="Author",
            surname="User",
            phone="+79009876543",
        )
        self.project = Project.objects.create(
            name="Django App",
            description="Cool project",
            owner=self.user,
            status="open",
            github_url="https://github.com/example/repo",
        )
        self.project.participants.add(self.user)
        self.client = Client()

    def test_project_detail_page(self):
        response = self.client.get(
            reverse("projects:detail", kwargs={"project_id": self.project.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django App")

    def test_complete_project(self):
        self.client.login(username="author@example.com", password="pass12345")
        response = self.client.post(
            reverse("projects:complete", kwargs={"project_id": self.project.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "closed")
