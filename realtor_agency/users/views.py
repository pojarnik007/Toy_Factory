from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import User

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm
from django.views.generic import TemplateView
import calendar
from django.utils import timezone

def employee_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_employee())(view_func)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:login')
        return render(request, 'users/register.html', {'form': form})
    return render(request, 'users/register.html', {'form': CustomUserCreationForm()})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('users:profile')
        return render(request, 'users/login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})



class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        timezone.activate(user.timezone if user.is_authenticated else 'UTC')

        today = timezone.localtime(timezone.now())
        cal = calendar.HTMLCalendar()
        context['calendar'] = cal.formatmonth(
            today.year,
            today.month,
            withyear=True
        )

        if user.is_authenticated:
            context['reviews'] = user.review_set.all().order_by('-time')
            # context['sales'] = Sale.objects.filter(client=user)
            client = getattr(user, 'client', None)
            if client:
                context['orders'] = client.orders.all().order_by('-order_date')
            else:
                context['orders'] = []
        return context
    
def user_profile(request, name):
    user = get_object_or_404(User, username=name) 
    return render(request, 'users/user_profile.html', context={'user': user})
    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})
