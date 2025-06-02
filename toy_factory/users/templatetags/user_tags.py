from django import template
from django.template.defaulttags import register
from users.models import User, Position

register = template.Library()

@register.filter
def is_employee(user):
    if not user.is_authenticated:
        return False
    return user.position == Position.EMPLOYEE.value

@register.filter
def is_admin(user):
    if not user.is_authenticated:
        return False
    return user.position == Position.ADMIN.value

@register.filter
def is_client(user):
    # Поддержка анонимного пользователя
    if not hasattr(user, "position"):
        return False
    return str(user.position) == "client"