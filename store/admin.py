from django.contrib import admin
from .models import Category,Payment,Product,Order,CancelOrder,CartItem,Cart

admin.site.register([CancelOrder,Order,Payment,Product,Category,CartItem,Cart])