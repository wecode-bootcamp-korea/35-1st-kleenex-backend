from django.db import models

from products.models import Products, Sizes, Grainding
from users.models    import User
from core.models     import TimeStampModel

class Carts(TimeStampModel): 
    username = models.ForeignKey(User, on_delete      = models.CASCADE)
    product  = models.ForeignKey(Products, on_delete  = models.CASCADE)
    size     = models.ForeignKey(Sizes, on_delete     = models.CASCADE)
    graind   = models.ForeignKey(Grainding, on_delete = models.CASCADE)
    quantity = models.IntegerField()
