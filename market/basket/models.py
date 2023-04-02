from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self, client_id, password, **extra_fields):
        if not client_id:
            raise ValueError('The Email must be set')
        user = self.model(client_id=client_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, client_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(client_id, password, **extra_fields)

class User(AbstractUser):

    username=None
    email = models.EmailField(("Email Address"))
    client_id = models.CharField(max_length=100,primary_key=True)
    last_transaction = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'client_id'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.client_id

    @property
    def token(self):
        token = Token.objects.get(user=User.objects.get(self.id))
        return token
    

class Product(models.Model):
    item_name = models.CharField(max_length=100, unique=True)
    price = models.FloatField(blank=True, null=True)
    season = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.item_name
    
class Order(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()

    def __str__(self):
        return self.order_id
    
    class Meta:
        unique_together = ('order_id', 'order_date')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.item_name.item_name

    class Meta:
        unique_together = ('order', 'item_name')

class Coupon(models.Model):
    COUPON_FORMAT_CHOICES = (
        ('alphanumeric', 'Alphanumeric'),
        ('numeric', 'Numeric'),
        ('alphabetic', 'Alphabetic'),
    )

    COUPON_DISCOUNT_CHOICES = (
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
    )

    code = models.CharField(max_length=100, unique=True)
    format = models.CharField(max_length=20, choices=COUPON_FORMAT_CHOICES, default='alphanumeric')
    discount_type = models.CharField(max_length=20, choices=COUPON_DISCOUNT_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=12, decimal_places=2)
    expiry_date = models.DateTimeField(blank=True, null=True)
    used = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , blank=True, null=True)
    
    def __str__(self):
        return self.code
    

class Redemption(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coupon.code
    
class MarketBasketCharts(models.Model):
    chart_name = models.CharField(max_length=100,)
    chart_created_at = models.DateTimeField(auto_now_add=True)
    chart_updated_at = models.DateTimeField(auto_now=True)
    chart_image = models.ImageField(upload_to='charts/', blank=True, null=True)

    def __str__(self):
        return self.chart_name
    
class AssociationRules(models.Model):
    consequent = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    antecedents = models.JSONField(max_length=100,)
    confidence = models.FloatField()

    def __str__(self):
        return self.confidence
    
class RFMTable(models.Model):
    rfm_segment = models.CharField(max_length=100, unique=True)
    recency = models.FloatField()
    frequency = models.FloatField()
    monetary = models.FloatField()

    def __str__(self):
        return self.rfm_segment