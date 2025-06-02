from django.db import models

class PromoCode(models.Model):
    text = models.CharField(unique=True, max_length=50, verbose_name="Промокод")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Скидка (%)")
    STATE_CHOICES = [
        ('active', 'Активен'),
        ('archive', 'Архив'),
    ]
    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        default='active',
        verbose_name="Статус"
    )

    def __str__(self):
        return f"{self.text} ({self.discount_percent}%)"