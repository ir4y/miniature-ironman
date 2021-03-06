# -*- coding: utf-8 -*-
import pytils
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from miniature.models.fields import AutoSlugField
from miniature.models.utils import create_model

__author__ = 'ir4y'


class ActiveManager(models.Manager):
    def active(self):
        return super(ActiveManager, self).get_queryset()\
                                         .filter(is_active='True')


class ActiveMixin(models.Model):
    is_active = models.BooleanField(verbose_name=_(u'Активно'), default=False)
    objects = ActiveManager()

    class Meta:
        abstract = True


class CreateUpdateMixin(models.Model):
    create = models.DateTimeField(auto_now_add=True,
                                  verbose_name=_(u'Дата создания'))
    update = models.DateTimeField(auto_now=True,
                                  verbose_name=_(u'Дата изменения'))

    class Meta:
        abstract = True


class SEOTagsMixin(models.Model):
    keywords = models.TextField(verbose_name=_(u'Ключевые слова'),
                                blank=True, null=True)
    description = models.TextField(verbose_name=_(u'Описание'),
                                   blank=True, null=True)

    class Meta:
        abstract = True


class GenericRelationMixin(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


def SlugTraits(base_filed_name='name'):
    """
    Функция генерирующая Mixin к модели
    Добавлющий _slug поле к указанному полю
    При сохраении в это поле записывается slug от указанного поля
    Описание класса на метаязыке
    class SlugMixin(models.Model):
        base_filed_name + '_slug' = models.CharField(
            verbose_name=_(u'Название для url'),max_length=150,
            blank=True,null=True)
        class Meta:
            abstract = True
    """
    fileld_name = base_filed_name + '_slug'
    fields = {
        fileld_name: AutoSlugField(verbose_name=_(u'Название для url'),
                                   populate_from='{' + base_filed_name + '}',
                                   max_length=150, blank=True, null=True)
    }
    _SlugMixin = create_model('SlugMixin', fields=fields,
                              module='miniature.models.mixins',
                              options={'abstract': True})
    return _SlugMixin
