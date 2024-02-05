from django.db import models
from django.conf import settings
from django.utils import timezone


class AnonimReader(models.Model):
    read_date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.device_id


class Article(models.Model):
    article_title = models.CharField(name="Title", max_length=50)
    article_subtitle = models.CharField(name="Subtitle", max_length=50)
    article_text = models.TextField(name="Text")
    short_text = models.CharField(name="ShortText", max_length=140)
    views = models.ManyToManyField(AnonimReader, blank=True)
    pub_date = models.DateTimeField(name="PublicDate", default=timezone.now())


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             default=None,
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=0)
