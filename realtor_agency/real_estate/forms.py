from django import forms

from django import forms
from .models import RealEstateObject, ObjectCategory

class RealEstateObjectForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=ObjectCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = RealEstateObject
        fields = ['title', 'description', 'location', 'price', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput()
        }
        labels = {
            'image': 'Изображение объекта'
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Цена должна быть положительным числом")
        return price

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = instance.create_slug(source_field='title')
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    