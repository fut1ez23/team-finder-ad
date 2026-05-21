from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.avatar import generate_avatar
from users.managers import UserManager

SKILL_NAME_MAX_LENGTH = 124
USER_NAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256


class Skill(models.Model):
    name = models.CharField(
        max_length=SKILL_NAME_MAX_LENGTH,
        verbose_name="Название",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name="Имя")
    surname = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар")
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH, verbose_name="Телефон")
    github_url = models.URLField(blank=True, verbose_name="GitHub")
    about = models.TextField(max_length=USER_ABOUT_MAX_LENGTH, blank=True, verbose_name="О себе")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    skills = models.ManyToManyField(
        Skill,
        related_name="users",
        blank=True,
        verbose_name="Навыки",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if self.pk is None and not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)