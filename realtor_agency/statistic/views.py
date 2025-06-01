from django.shortcuts import render
from .services import get_statistics_context
from users.decorators import *
from users.models import Position

@role_required([Position.ADMIN])
def statistics_view(request):
    context = get_statistics_context()
    return render(request, 'statistic/statistic.html', context)
