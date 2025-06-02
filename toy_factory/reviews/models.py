from django.db import models
from users.models import User

class Review(models.Model):
    title = models.CharField()
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    RATING_CHOICES = [(x, str(x)) for x in range(1,11)]
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name='оценка')
    
    def __str__(self):
        return self.title
