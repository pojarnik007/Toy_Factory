from django.shortcuts import render, redirect, get_object_or_404
from .models import PromoCode
from django.contrib.auth.decorators import user_passes_test
from .forms import PromoCodeForm

def is_admin(user):
    return user.is_authenticated and getattr(user, "position", "") == "admin"

@user_passes_test(is_admin)
def promocodes(request):
    promocodes = PromoCode.objects.all()
    return render(request, 'promotions/promocodes.html', context={'promocodes': promocodes})

@user_passes_test(is_admin)
def promocode_add(request):
    if request.method == "POST":
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promotions:promocodes')
    else:
        form = PromoCodeForm()
    return render(request, 'promotions/promocode_add.html', {'form': form})

@user_passes_test(is_admin)
def promocode_delete(request, pk):
    promocode = get_object_or_404(PromoCode, pk=pk)
    if request.method == "POST":
        promocode.delete()
        return redirect('promotions:promocodes')
    return render(request, 'promotions/promocode_delete.html', {'promocode': promocode})