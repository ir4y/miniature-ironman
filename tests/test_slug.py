# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from models import Product


@pytest.mark.django_db
def test_slug_generator():
    product = Product.objects.create(name=u'название')
    assert product.name_slug == 'nazvanie'
