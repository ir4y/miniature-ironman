from django.db import models
from miniature.models.mixins import SlugTraits


class Product(SlugTraits(), models.Model):
    name = models.CharField(max_length=100)
