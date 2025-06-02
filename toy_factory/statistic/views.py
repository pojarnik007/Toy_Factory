from django.shortcuts import render
from .services import get_statistics_context
from users.models import Position
from users.decorators import role_required

@role_required([Position.ADMIN, Position.EMPLOYEE])
def statistics_view(request):
    context = get_statistics_context()
    return render(request, 'statistic/statistic.html', context)