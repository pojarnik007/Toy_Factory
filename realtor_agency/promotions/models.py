from django.db import models

class PromoCode(models.Model):
    text = models.CharField()
    STATE_CHOICES = [
        ('active', 'Active'),
        ('archive', 'Archive'),
    ]
    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
    )

    def __str__(self):
        return self.text
