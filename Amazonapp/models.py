from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileno = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Address(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    country=models.CharField(max_length=20)
    fullname=models.CharField(max_length=64)
    mobileno = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    pincode=models.CharField(max_length=10)
    street=models.CharField(max_length=200)
    landmark=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    address_type=models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def  __str__(self):
        return self.fullname

class Category(models.Model):
    title = models.CharField(max_length=200)
    active= models.BooleanField(default=True)
    image = models.ImageField(upload_to='products', null=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products', null=True)
    description = models.CharField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    rating= models.IntegerField()
    units = models.IntegerField()
    image=models.ImageField(upload_to='products', null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    #user = models.ManyToManyField(User)

    def __str__(self):
        return self.title

class Cart(models.Model):
    subtotal = models.IntegerField()
    total = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products=models.ManyToManyField(Product, blank=True)
    def __str__(self):
        return str(self.id)

class Cart1(models.Model):
    units=models.IntegerField()
    subtotal=models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Order(models.Model):
    units = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
