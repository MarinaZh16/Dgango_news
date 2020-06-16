from django.contrib import admin
from . import models
from articles import models as art_models
# Register your models here.


class ArticlesInline(admin.TabularInline):
    model = art_models.Article
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ArticlesInline]


admin.site.register(models.User, UserAdmin)