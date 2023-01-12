from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    bio = models.TextField()
    profile_user_id = models.BigIntegerField()
    image = models.ImageField(upload_to="profiles", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


class Supplier(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="suppliers", blank=True)
    contact_info = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to="products", blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    latitude = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="locations", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} {self.longitude} {self.latitude}"


class Buyer(models.Model):
    name = models.CharField(max_length=250)
    contact_info = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True)
    quantity = models.FloatField(default=1)
    description = models.TextField(blank=True)
    order_type = models.CharField(max_length=250)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.product.name} {self.location.name}"


class Insurance(models.Model):
    company_name = models.CharField(max_length=250)
    contact_info = models.CharField(max_length=250)
    price = models.FloatField(default=0)
    description = models.TextField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.company_name


class Guarantee(models.Model):
    month_duration = models.FloatField(default=0)
    description = models.TextField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.product.name} {self.month_duration}"


class Comment(models.Model):
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.message
