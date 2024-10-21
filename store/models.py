from django.db import models
from django.utils.text import slugify
from django.db.models import SlugField
from django.contrib.auth.models import User



class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    prod_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='uploads/product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.prod_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.prod_name

class Order(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming you are using the default User model
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    product_list = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f'Order {self.id} by {self.user_id.username}'

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you're using Django's default User model
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_list = models.ManyToManyField('Product', through='CartItem', related_name='carts')

    def __str__(self):
        return f'Cart for {self.user_id.username}'

# Intermediate model for handling the product quantity in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.prod_name} in cart'

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f'Payment for Order {self.order.id}'

class CancelOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f'Cancel Order {self.id} for Order {self.order.id}'

class Boutique(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name
