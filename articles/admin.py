from django.contrib import admin
from . import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category']
    list_editable = ['title', 'category']
    row_id_fields = ['author']


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category)
admin.site.register(models.Channel)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
# Register your models here.
