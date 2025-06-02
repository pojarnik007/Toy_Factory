from django.db import models
from users.models import User

class Contact(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='contact/')

    def __str__(self):
        return self.name
