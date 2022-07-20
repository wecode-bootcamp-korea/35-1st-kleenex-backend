from django.db import models

from products.models import Product, Size, Grainding
from users.models    import User
from core.models     import TimeStampModel

class Order(TimeStampModel): 
    order_number = models.CharField(max_length = 250)
    username     = models.ForeignKey(User,      on_delete = models.CASCADE)
    status       = models.ForeignKey('Status',  on_delete = models.CASCADE)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model): 
    product      = models.ForeignKey(Product,   on_delete = models.CASCADE)
    size         = models.ForeignKey(Size,      on_delete = models.CASCADE)
    graind       = models.ForeignKey(Grainding, on_delete = models.CASCADE)
    order        = models.ForeignKey('Order',   on_delete = models.CASCADE)
    quantity     = models.IntegerField()

    class Meta:
        db_table = 'orderitems'



class Status(models.Model): 
    name         = models.CharField(max_length = 20)

    class Meta:
        db_table = 'statuses'
