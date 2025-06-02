from django import forms
from .models import Toy, ToyType, Manufacturer

class ToyForm(forms.ModelForm):
    class Meta:
        model = Toy
        fields = [
            'image',        # Фото
            'name',         # Название
            'code',         # Артикул
            'toy_type',     # Вид игрушки
            'description',  # Описание
            'manufacturer', # Производитель
            'price',        # Цена
            'is_active',    # В продаже
            'in_stock',     # В наличии
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'image': 'Фото',
            'name': 'Название',
            'code': 'Артикул',
            'toy_type': 'Вид игрушки',
            'manufacturer': 'Производитель',
            'description': 'Описание',
            'price': 'Цена',
            'is_active': 'В продаже',
            'in_stock': 'В наличии',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть положительным числом")
        return price

    def clean_in_stock(self):
        stock = self.cleaned_data.get('in_stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("Количество в наличии не может быть отрицательным")
        return stock

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            qs = Toy.objects.filter(code=code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Игрушка с таким артикулом уже существует")
        return code