from django.db import models
from django.conf import settings
import uuid as uuid
USER_MODEL = settings.AUTH_USER_MODEL


class TimeStampMode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Article(TimeStampMode):
    title = models.CharField(max_length=80, verbose_name="Название")
    text = models.TextField()
    author = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    channel = models.ForeignKey('Channel', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField('Tag')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def add_like(self, user):
        like_exists = self.likes_set.filter(user=user).exists()
        if like_exists:
            self.likes_set.get(user=user, article_id=self.id).delete()
        else:
            self.likes_set.create(user=user, article=self)


class Channel(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class Comment(TimeStampMode):
    text = models.CharField(max_length=256)
    author = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='comments')

    def __str__(self):
        return f"{self.text}, {self.author}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE,
                               related_name='child_categories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"


class Likes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
