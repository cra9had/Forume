from django.contrib import admin
from .models import Article, AnonimReader, Like

admin.site.register(Article)
admin.site.register(AnonimReader)
admin.site.register(Like)
# Register your models here.
