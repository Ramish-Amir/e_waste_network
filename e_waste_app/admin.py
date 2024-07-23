from django.contrib import admin
from .models import Member, ContactMessage, RecycleItem, Feedback, Article


# Register your models here.

admin.site.register(ContactMessage),
admin.site.register(RecycleItem)
admin.site.register(Member)
admin.site.register(Article)
admin.site.register(Feedback)
