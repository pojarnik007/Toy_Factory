from django.db import models
from django.utils.text import slugify
from transliterate import translit

class SlugMixin:
    def create_slug(self, source_field, slug_field='slug'):
        source_text = getattr(self, source_field)
        transliterated = translit(source_text, 'ru', reversed=True)
        base_slug = slugify(transliterated)
        unique_slug = base_slug
        counter = 1
        
        while self.__class__.objects.filter(**{slug_field: unique_slug}).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
            
        return unique_slug