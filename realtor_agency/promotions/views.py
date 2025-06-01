from django.shortcuts import render
from .models import PromoCode

def promocodes(request):
    promocodes = PromoCode.objects.all()
    return render(request, 'promotions/promocodes.html', context={'promocodes': promocodes})
