from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Member(User):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    e_waste_interests = models.TextField(blank=True, null=True)
    recycling_preferences = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class RecyclingRequest(models.Model):
    CATEGORY_CHOICES = [
        ('consumer_electronics', 'Consumer Electronics'),
        ('home_appliances', 'Home Appliances'),
        ('office_equipment', 'Office Equipment'),
        ('medical_devices', 'Medical Devices'),
        ('industrial_equipment', 'Industrial Equipment'),
        ('miscellaneous_electronics', 'Miscellaneous Electronics'),
    ]

    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    item_type = models.CharField(max_length=50)
    description = models.TextField()
    condition = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='recycling_requests/', blank=True, null=True)

    def __str__(self):
        return f'{self.item_type} - {self.category}'
