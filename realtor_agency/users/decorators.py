from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles):
    def decorator(view_func):
        @login_required(login_url='users:login') 
        def wrapper(request, *args, **kwargs):
            if request.user.position in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Нет доступа")
        return wrapper
    return decorator