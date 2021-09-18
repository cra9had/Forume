from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Ip(models.Model): # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Article(models.Model):
    article_title = models.CharField(name="Title", max_length=50)
    article_subtitle = models.CharField(name="Subtitle", max_length=50)
    article_text = models.TextField(name="Text")
    views = models.ManyToManyField(Ip, related_name="Views", blank=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             default=None,
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=0)
