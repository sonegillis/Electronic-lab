from django.contrib import admin
from .models import EquipmentBorrowTransactions, ModemImeiNumber, Equipment, Category
# Register your models here.

admin.site.register(EquipmentBorrowTransactions)
admin.site.register(ModemImeiNumber)
admin.site.register(Equipment)
admin.site.register(Category)

admin.site.site_header = "Laboratory Management Administration"



