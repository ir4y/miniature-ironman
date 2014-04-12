# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from tests.models import Product, Item


@pytest.mark.django_db
def test_slugtraits():
    product = Product.objects.create(name='название')
    assert product.name_slug == 'nazvanie'


@pytest.mark.django_db
def test_autoslugfield():
    product = Product.objects.create(name='название')
    item = Item.objects.create(product=product,
                               title='элемент')
    assert item.slug == 'nazvanie-element'
