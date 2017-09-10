from buc import models
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    exclude = ('editor',)

    def save_model(self, request, obj, form, change):
        obj.Editor = request.user
        obj.save()


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(100, 30)]
    format = 'JPEG'
    options = {'quality': 60 }

def cached_admin_thumb(instance):
    # `image` is the name of the image field on the model
    cached = ImageCacheFile(AdminThumbnailSpec(instance.image))
    # only generates the first time, subsequent calls use cache
    cached.generate()
    return cached


class ArticlePhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')

admin.site.register(models.ArticlePhoto, ArticlePhotoAdmin)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Profile)
 