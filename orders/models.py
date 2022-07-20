from django.db import models

from products.models import Products, Sizes, Grainding
from users.models    import User
from core.models     import TimeStampModel

class Orders(TimeStampModel): 
    order_number = models.CharField(max_length=250)
    username     = models.ForeignKey(User, on_delete       = models.CASCADE)
    status       = models.ForeignKey('Statuses', on_delete = models.CASCADE)

class OrderItems(models.Model): 
    product  = models.ForeignKey(Products, on_delete  = models.CASCADE)
    size     = models.ForeignKey(Sizes, on_delete     = models.CASCADE)
    graind   = models.ForeignKey(Grainding, on_delete = models.CASCADE)
    order    = models.ForeignKey('Orders', on_delete  = models.CASCADE)
    quantity = models.IntegerField()


class Statuses(models.Model): 
    status = models.CharField(max_length=150)