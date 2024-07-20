from django.contrib import admin
from .models import Member, ContactMessage, Product, RecycleItem


# Register your models here.

admin.site.register(ContactMessage),
admin.site.register(Product)


admin.site.register(RecycleItem)
admin.site.register(Member)
