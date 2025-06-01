from django.db import models
from .mixins import SlugMixin
from users.models import User


class RealEstateObject(models.Model, SlugMixin):
    title = models.CharField(max_length=255)
    slug = models.CharField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_slug(source_field='title')
        super().save(*args, **kwargs)

    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ManyToManyField("ObjectCategory")
    image = models.ImageField(upload_to='object/')
    on_sale = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ObjectCategory(models.Model, SlugMixin):
    name = models.CharField(max_length=255)
    slug = models.CharField(primary_key=True, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_slug(source_field='name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Sale(models.Model):
    real_estate_object = models.ForeignKey(RealEstateObject, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)
    contract_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.real_estate_object} продан клиенту {self.client} {self.sale_date}"


