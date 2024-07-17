from datetime import timezone

from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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


class RecyclingRequest(models.Model):
    CATEGORY_CHOICES = [
        ('consumer_electronics', 'Consumer Electronics'),
        ('home_appliances', 'Home Appliances'),
        ('office_equipment', 'Office Equipment'),
        ('medical_devices', 'Medical Devices'),
        ('industrial_equipment', 'Industrial Equipment'),
        ('miscellaneous_electronics', 'Miscellaneous Electronics'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    item_type = models.CharField(max_length=50)
    description = models.TextField()
    condition = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_posted = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    use_contact_details = models.BooleanField(default=False)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_address = models.CharField(max_length=300, blank=True, null=True)
    contact_city = models.CharField(max_length=50, blank=True, null=True)
    contact_province = models.CharField(max_length=50, blank=True, null=True)
    contact_postal_code = models.CharField(max_length=20, blank=True, null=True)
    contact_country = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='recycling_requests/', blank=True, null=True)

    def __str__(self):
        return f'{self.item_type} - {self.category}'

