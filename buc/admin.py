from django.db import models
from django.contrib import admin

admin.site.register(models.Article)

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    exclude = ('editor',)

    def save_model(self, request, obj, form. change):
        obj.Editor = request.user
        obj.save()

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article, ArticleAdmin)
