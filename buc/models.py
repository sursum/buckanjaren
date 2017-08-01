from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Tag, self).save()

    def get_absolute_url(self):
        return "/tag/%s/" % (self.slug)

    def __unicode__(self):
        return self.name

class Category(models.Model)
    name = models.CharField(max_length=20)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Category, self).save()

    def get_absolute_url(self):
        return "/category/%s/" % (self.slug)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Article(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField()
    text = models.TextField()
    comment = models.TextField()
    author =
    editor = models.ForeignKey(User)
    commentator =
    slug = models.SlugField(max_length=40, unique=True)
    site = models.ForeignKey(Site)
    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.slug)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]
