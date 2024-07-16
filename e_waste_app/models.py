from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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
