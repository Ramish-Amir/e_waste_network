from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Member(User):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(blank=True,max_length=50)
    province = models.CharField(blank=True,max_length=50)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(blank=True,max_length=50, null=True)
    user_type = models.CharField(blank=True,max_length=20, choices=USER_TYPE_CHOICES)
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


class RecycleItem(models.Model):
    CATEGORY_CHOICES = [
        ('consumer_electronics', 'Consumer Electronics'),
        ('home_appliances', 'Home Appliances'),
        ('office_equipment', 'Office Equipment'),
        ('medical_devices', 'Medical Devices'),
        ('industrial_equipment', 'Industrial Equipment'),
        ('miscellaneous_electronics', 'Miscellaneous Electronics'),
    ]

    CONDITION_CHOICES = [
        ('working', 'Working'),
        ('not_working', 'Not Working'),
        ('partial_working', 'Partial Working'),
    ]

    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    item_type = models.CharField(max_length=50)
    description = models.TextField()
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='recycling_items/', blank=True, null=True)

    def __str__(self):
        return f'{self.item_type} - {self.category}'


#UserHistory
class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_start = models.DateTimeField()
    visit_end = models.DateTimeField(null=True, blank=True)
    visit_duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.visit_end and not self.visit_duration:
            self.visit_duration = self.visit_end - self.visit_start
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.visit_start} to {self.visit_end}'