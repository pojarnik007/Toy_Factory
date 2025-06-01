from django.db import models


class Vacancy(models.Model):
    title = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.title
