from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import Skill, User


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей и проекты"

    def handle(self, *args, **options):
        skills_data = ["Python", "Django", "JavaScript", "React", "PostgreSQL"]
        skills = [Skill.objects.get_or_create(name=name)[0] for name in skills_data]

        admin, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "name": "Admin",
                "surname": "User",
                "phone": "+79000000000",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("testpass123")
            admin.save()

        users_data = [
            ("anna@example.com", "Анна", "Иванова", "+79001111111"),
            ("boris@example.com", "Борис", "Петров", "+79002222222"),
            ("clara@example.com", "Клара", "Сидорова", "+79003333333"),
        ]

        users = []
        for email, name, surname, phone in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"name": name, "surname": surname, "phone": phone},
            )
            if created:
                user.set_password("testpass123")
                user.save()
            users.append(user)

        users[0].skills.set(skills[:2])
        users[1].skills.set(skills[1:4])
        users[2].skills.set([skills[4]])

        for index, user in enumerate(users):
            if not user.owned_projects.exists():
                project = Project.objects.create(
                    name=f"Проект {user.name}",
                    description=f"Описание проекта от {user.name}",
                    owner=user,
                    status="open",
                    github_url="https://github.com/example/repo",
                )
                project.participants.add(user)
                if index > 0:
                    project.participants.add(users[0])

        self.stdout.write(self.style.SUCCESS("Тестовые данные созданы"))
