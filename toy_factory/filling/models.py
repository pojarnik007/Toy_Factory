from turtle import up
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from transliterate import translit
from django.utils.text import slugify

from django.db import models
from django.urls import reverse
from transliterate import translit
from django.utils.text import slugify


# filling/models.py

from django.db import models
# ... other imports

# filling/models.py

from django.db import models
from django.urls import reverse
from transliterate import translit
from django.utils.text import slugify

# --- Модель Компании ---
class CompanyInformation(models.Model):
    description = models.TextField(verbose_name="Описание компании")
    logo = models.ImageField(upload_to='company/', verbose_name="Логотип", null=True, blank=True)
    video = models.FileField(upload_to='company_video/', verbose_name="Видео-презентация", null=True, blank=True)
    inn = models.CharField(max_length=12, verbose_name="ИНН", null=True, blank=True)
    kpp = models.CharField(max_length=9, verbose_name="КПП", null=True, blank=True)
    bik = models.CharField(max_length=9, verbose_name="БИК", null=True, blank=True)
    account_number = models.CharField(max_length=20, verbose_name="Расчётный счёт", null=True, blank=True)
    certificate_image = models.ImageField(upload_to='company_certs/', verbose_name="Изображение сертификата", null=True, blank=True)
    certificate_caption = models.CharField(max_length=255, verbose_name="Подпись к сертификату", null=True, blank=True)

    def __str__(self):
        return "Основная информация о компании"
    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

# --- Модель Истории ---
class CompanyHistory(models.Model):
    year = models.PositiveIntegerField(verbose_name="Год")
    event = models.TextField(verbose_name="Событие")
    class Meta:
        ordering = ["year"]
        verbose_name = "Историческое событие"
        verbose_name_plural = "История компании"
    def __str__(self):
        return f"{self.year}: {self.event[:50]}"

# --- Модель Партнера (используем ее) ---
class Partner(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название партнёра")
    logo = models.ImageField(upload_to="partners/", verbose_name="Логотип")
    website = models.URLField(verbose_name="Сайт партнёра")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

# --- Остальные модели (FAQ, Article) остаются без изменений ---
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
            transliterated_title = translit(self.title, 'ru', reversed=True)
            self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('filling:article', kwargs={'slug': self.slug})

    # --- ДОБАВИТЬ В КОНЕЦ ФАЙЛА filling/models.py ---

class SliderSettings(models.Model):
        """Настройки слайдера (синглтон, чтобы была только одна запись)"""
        delay = models.PositiveIntegerField(
            default=5000,
            verbose_name="Время показа слайда (мс)",
            help_text="Введите время в миллисекундах (например, 5000 = 5 сек)"
        )
        is_auto = models.BooleanField(default=True, verbose_name="Автоматическое переключение")
        is_loop = models.BooleanField(default=True, verbose_name="Бесконечная прокрутка")

        def __str__(self):
            return "Настройки слайдера"

        class Meta:
            verbose_name = "Настройки слайдера"
            verbose_name_plural = "Настройки слайдера"

class PromoSlide(models.Model):
        """Отдельный слайд"""
        title = models.CharField(max_length=255, verbose_name="Заголовок слайда")
        image = models.ImageField(upload_to='slides/', verbose_name="Изображение")
        link = models.CharField(max_length=255, verbose_name="Ссылка при клике (URL)", default="#")
        order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

        class Meta:
            ordering = ['order']
            verbose_name = "Слайд"
            verbose_name_plural = "Слайды"

        def __str__(self):
            return self.title