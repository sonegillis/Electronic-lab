from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
# Create your models here.

class EquipmentBorrowTransactions(models.Model):
    matricule = models.CharField(max_length=8)
    tel = models.CharField(max_length=14)
    given_date = models.DateField(auto_now_add=True)
    ret_date = models.DateField()
    given_by = models.ForeignKey(User, related_name="%(class)s_given_by")
    item = models.CharField(max_length=100)
    quantity = models.IntegerField()
    returned = models.BooleanField(default=False)
    returned_to = models.ForeignKey(User, related_name="%(class)s_returned_to", null=True)

    def __str__(self):
        return self.matricule

class Category(models.Model):
    library = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.library

class Equipment(models.Model):
    library = models.ForeignKey(Category)
    component = models.CharField(max_length=100)

    def __str__(self):
        return self.component


class ModemState(models.Model):
    state = models.BooleanField(default=False)


class ModemImeiNumber(models.Model):
    mtn_key_imei = models.CharField(max_length=100)
    orange_key_imei = models.CharField(max_length=100)

    def __str__(self):
        return "MODEM IMEI NUMBER"

