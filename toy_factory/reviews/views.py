from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Review
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm


def index(request):
    reviews = Review.objects.all().order_by('-time')
    return render(request, 'reviews/index.html', {'reviews': reviews})

@login_required
def create(request):
    if request.method == 'POST':
        review = Review()
        review.title = request.POST.get('title')
        review.text = request.POST.get('text')
        review.rating = request.POST.get('rating')
        review.user = request.user
        review.save()
        return redirect('reviews:index')
    return render(request, 'reviews/create.html', {'rating_choices': Review.RATING_CHOICES})

@login_required
def edit(request, id):
    review = get_object_or_404(Review, id=id)
    
    if review.user != request.user:
        return HttpResponseForbidden("У вас нет прав для редактирования этого отзыва")
    
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.text = request.POST.get('text')
        review.rating = request.POST.get('rating')
        review.save()
        return redirect('reviews:index')
    
    return render(request, 'reviews/edit.html', {
        'review': review,
        'rating_choices': Review.RATING_CHOICES
    })

@login_required
def delete(request, id):
    review = get_object_or_404(Review, id=id)
    
    if review.user != request.user:
        return HttpResponseForbidden("У вас нет прав для удаления этого отзыва")
    
    review.delete()
    return redirect('reviews:index')





