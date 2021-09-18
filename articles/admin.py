from django.contrib import admin
from .models import Article, Ip, Like

admin.site.register(Article)
admin.site.register(Ip)
admin.site.register(Like)
# Register your models here.
