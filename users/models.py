from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name         = models.CharField(max_length = 50)
    username     = models.CharField(max_length = 100, unique = True)
    password     = models.CharField(max_length = 250)
    address      = models.CharField(max_length = 150)
    email        = models.CharField(max_length = 150, unique = True)
    phone_number = models.CharField(max_length = 50,  unique = True)

    class Meta:
        db_table = 'users'
