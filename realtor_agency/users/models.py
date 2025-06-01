# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django import utils
from django.core.exceptions import ValidationError
from datetime import date
from pytz import common_timezones

phone_validator = RegexValidator(
    regex=r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$',
    message="Номер должен быть в формате +375 (ZZ) XXX-XX-XX"
)


class Position(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    CLIENT = 'client', 'Client'
    EMPLOYEE = 'employee', 'Employee'


class User(AbstractUser):
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        blank=True,
        help_text="+375 (ZZ) XXX-XX-XX",
        unique=True,
        error_messages={
            'unique': "Пользователь с таким номером уже существует."
        }
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="DD/MM/YYYY"
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует."
        }
    )

    TIMEZONE_CHOICES = [(tz, tz) for tz in common_timezones]
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='UTC',
        verbose_name="Часовой пояс"
    )

    @property
    def age(self):
        if not self.date_of_birth:
            return 0
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < 
            (self.date_of_birth.month, self.date_of_birth.day)
        )

    def clean(self):
        super().clean()
        if not self.date_of_birth:
            raise ValidationError("Дата рождения обязательна")
        if self.age < 18:
            raise ValidationError("Пользователь должен быть старше 18 лет")

    groups = models.ManyToManyField(
        Group,
        verbose_name="Группы",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь",
        related_name="custom_user_groups",  # Уникальное имя
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="Права пользователя",
        blank=True,
        help_text="Специальные права для пользователя",
        related_name="custom_user_permissions",  # Уникальное имя
        related_query_name="user",
    )

    position = models.CharField(max_length=100, blank=True, choices=Position.choices, default=Position.CLIENT)
    hire_date = models.DateField(default=utils.timezone.now, blank=True, null=True)


