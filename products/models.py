from django.db import models

from core.models import TimeStampModel


class Categories(models.Model): 
    name = models.CharField(max_length=50)


class SubCategories(models.Model): 
    name     = models.CharField(max_length=50)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)


class Products(TimeStampModel):
    name         = models.CharField(max_length=150, unique=True)
    eng_name     = models.CharField(max_length=250, unique=True)
    rosting_date = models.DateField()
    price        = models.DecimalField()


class ProductImages(models.Model):
    url     = models.CharField(max_length=300)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)


class Sizes(models.Model): 
    size    = models.CharField(max_length=50)
    price   = models.DecimalField()
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    

class Tastes(models.Model): 
    tastes          = models.CharField(max_length=50)
    products_tastes = models.ManyToManyField(
        'Products', related_name = 'taste'
    )


class Grainding(models.Model): 
    type               = models.CharField(max_length=100)
    products_grainding = models.ManyToManyField(
        'Products', related_name = 'graind'
    )