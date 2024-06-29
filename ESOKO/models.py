from django.db import models
import uuid
from ckeditor.fields import RichTextField
# Create your models here.
class Product_Category(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name=models.CharField(max_length=255,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    def get_category_products(self):
        return self.product_set.all()
    class Meta:
        
        verbose_name_plural='Product Categories'
class Product(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=255)
    slug=models.CharField(max_length=255,null=True,blank=True)
    category=models.ForeignKey(Product_Category,on_delete=models.CASCADE,null=True,blank=True)
    description=RichTextField()
    price=models.IntegerField(null=True, blank=True)
    thumbnail=models.ImageField(upload_to='products/thumbnails')
    location=models.CharField(max_length=255)
    contact=models.CharField(max_length=40)
    valid=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    bought=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.created_at}"
class Product_Esoko(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title = models.CharField(max_length=255)
    slug=models.CharField(max_length=255,null=True,blank=True)
    category=models.ForeignKey(Product_Category,on_delete=models.CASCADE,null=True,blank=True)
    description=RichTextField()
    product_price=models.IntegerField(null=True, blank=True)
    thumbnail=models.ImageField(upload_to='products/thumbnails')
    product_location=models.CharField(max_length=255)
    owner_contact=models.CharField(max_length=40)
    valid=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    bought=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.created_at}"    
