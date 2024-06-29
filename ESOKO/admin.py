from django.contrib import admin
from .models import Product_Category,Product,Product_Esoko
# Register your models here.
admin.site.register(Product)
admin.site.register(Product_Esoko)
admin.site.register(Product_Category)