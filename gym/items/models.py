from ast import Or
from PIL import Image
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    image=models.ImageField(null=True,blank=True)
    is_digital=models.BooleanField(default=False,null=True,blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)    
   

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    is_completed=models.BooleanField(default=False,null=True,blank=False)
    order_added=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        get_items=self.orderitems_set.all()
        total_items=sum(item.quantity for item in get_items)
        return total_items

    @property
    def get_cart_total(self):
        get_items=self.orderitems_set.all()
        total_items=sum(item.get_items_total for item in get_items)
        return total_items         

class OrderItems(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_items_total(self):
        total=self.product.price * self.quantity
        return total

class ShippingDetails(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=250,null=True)
    city=models.TextField(max_length=200,null=True)
    zip_code=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address    