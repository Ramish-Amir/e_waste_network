from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

from e_waste import settings
from django.utils import timezone
# Create your models here.


class Member(User):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(blank=True, max_length=50)
    province = models.CharField(blank=True, max_length=50)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(blank=True, max_length=50, null=True)
    user_type = models.CharField(blank=True, max_length=20, choices=USER_TYPE_CHOICES)
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
    use_profile_contact = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='recycling_items/', blank=True, null=True)

    def __str__(self):
        return f'{self.item_type} - {self.category}'


class Feedback(models.Model):
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.created_at}"


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('recycling', 'E-Waste Recycling'),
        ('impact', 'Environmental Impact'),
        ('innovation', 'Technology and Innovation'),
        ('awareness', 'Consumer Awareness'),
        ('health', 'Health Impacts'),
        ('devices', 'Electronic Devices'),
        ('best_practices', 'E-Waste Management Best Practices'),
    ]

    # ForeignKey to link the article to the user who created it
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='articles',blank=True, null=True)

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='impact')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserVisit(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Visit by {self.user} at {self.visit_time}'