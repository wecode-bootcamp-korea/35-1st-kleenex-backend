from django.db import models

from products.models import Product, Size, Grainding
from users.models    import User
from core.models     import TimeStampModel

class Cart(TimeStampModel): 
    user         = models.ForeignKey(User,      on_delete   = models.CASCADE)
    product      = models.ForeignKey(Product,   on_delete   = models.CASCADE)
    size         = models.ForeignKey(Size,      on_delete   = models.CASCADE)
    graind       = models.ForeignKey(Grainding, on_delete   = models.CASCADE)
    quantity     = models.IntegerField()

    class Meta:
        db_table = 'carts'
