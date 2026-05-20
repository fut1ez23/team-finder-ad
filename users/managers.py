import random

from django.contrib.auth.models import BaseUserManager

from users.avatar import generate_avatar


class UserManager(BaseUserManager):
    def _generate_unique_phone(self):
        while True:
            phone = f"+7{random.randint(1000000000, 9999999999)}"
            if not self.model.objects.filter(phone=phone).exists():
                return phone

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        extra_fields.setdefault("phone", self._generate_unique_phone())
        user = self.model(email=email, **extra_fields)
        if not user.avatar:
            user.avatar = generate_avatar(user.name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault("surname", "User")
        return self.create_user(email, password, **extra_fields)
