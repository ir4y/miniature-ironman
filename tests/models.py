from django.db import models
from miniature.models.fields import AutoSlugField
#, DenormalizeField
from miniature.models.mixins import SlugTraits


class Product(SlugTraits(), models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Item(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="{product}-{title}",
                         max_length=150)
