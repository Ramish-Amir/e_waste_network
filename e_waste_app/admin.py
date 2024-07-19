from django.contrib import admin
from .models import Member, ContactMessage, Product
# Register your models here.
admin.site.register(Member),
admin.site.register(ContactMessage),
admin.site.register(Product)
