from django.db import models

from realtors.models import Realtor


# Create your models here
class Account(models.Model):
    user = models.OneToOneField(Realtor, on_delete=models.CASCADE,  primary_key=True, )
    id = models.IntegerField()
    listing = models.CharField(max_length=200)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
