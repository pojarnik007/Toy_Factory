from django.db import models
from django.shortcuts import render
from users.models import User

class ToyType(models.Model):
    """Вид игрушки (тип изделия)"""
    name = models.CharField("Название типа", max_length=100)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField("Название производителя", max_length=100)
    country = models.CharField("Страна", max_length=100, blank=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name


class Toy(models.Model):
    """Игрушка (экземпляр для каталога и продаж)"""
    image = models.ImageField("Фото", upload_to="toys/", blank=True, null=True)
    name = models.CharField("Название", max_length=100)
    code = models.CharField("Артикул", max_length=30, unique=True)
    toy_type = models.ForeignKey(ToyType, on_delete=models.CASCADE, related_name="toys")
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    is_active = models.BooleanField("В продаже", default=True)
    in_stock = models.PositiveIntegerField("В наличии", default=0)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, related_name="toys", verbose_name="Производитель")

    def __str__(self):
        return f"{self.name} ({self.code})"

class Client(models.Model):
    """Покупатель"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Имя/Компания", max_length=150)
    phone = models.CharField("Телефон", max_length=20)
    city = models.CharField("Город", max_length=100, blank=True)
    email = models.EmailField("Email", blank=True)
    is_wholesale = models.BooleanField("Оптовый клиент", default=False)

    def __str__(self):
        return self.name

class PickupPoint(models.Model):
    """Точка самовывоза"""
    address = models.CharField("Адрес", max_length=255)
    description = models.TextField("Описание", blank=True)
    active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.address

from promotions.models import PromoCode
class Order(models.Model):
    """Заказ покупателя"""
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('processing', 'В обработке'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField("Количество", default=1)
    order_date = models.DateTimeField("Дата заказа", auto_now_add=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='created')
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField("Комментарий", blank=True)

    def __str__(self):
        return f"Заказ {self.id} ({self.client})"

class PromoCode(models.Model):
    """Промокод для скидок"""
    code = models.CharField("Код", max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField("Скидка %", default=0)
    active = models.BooleanField("Активен", default=True)
    expires_at = models.DateField("Действует до", null=True, blank=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

class SaleAnalytics(models.Model):
    """Аналитика продаж"""
    date = models.DateField("Дата")
    total_orders = models.PositiveIntegerField("Всего заказов")
    total_income = models.DecimalField("Сумма продаж", max_digits=12, decimal_places=2)
    most_popular_toy = models.ForeignKey(Toy, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return f"Аналитика {self.date}"

