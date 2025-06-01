from turtle import up
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from users.models import phone_validator
from transliterate import translit
from django.utils.text import slugify


class CompanyInformation(models.Model):
    description = models.TextField()


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.question


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='article/')
    time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = translit(self.title, 'ru', reversed=True)  # 'ru' → 'en'
            self.slug = slugify(transliterated_title)
        
        counter = 1
        while Article.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{counter}"
            counter += 1
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('filling:article', kwargs={'slug': self.slug})

