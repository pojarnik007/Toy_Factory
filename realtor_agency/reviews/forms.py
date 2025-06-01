from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','text', 'rating']
        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.Select(choices=Review.RATING_CHOICES)
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Ваш отзыв',
            'rating': 'Оценка'
        }