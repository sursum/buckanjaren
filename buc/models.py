from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class ArticlePhoto(models.Model):
    photo = models.ImageField(upload_to='ArticlePhoto/%Y/%m/%d')
    photo_thumbnail = ImageSpecField(source='ArticlePhoto/%Y/%m/%d',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})    

class Profile(models.Model):    
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    contact = models.EmailField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})


    def __str__(self):
        return self.author.username

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/tag/%s/" % (self.slug)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/category/%s/" % (self.slug)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Article(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateTimeField('date published',blank=True,null=True)
    created_date = models.DateTimeField('date created',default=datetime.now,blank=True,null=True)
    text = models.TextField()
    comment = models.TextField(blank=True,null=True)
    editor = models.ForeignKey(User,blank=True,null=True)
    creator = models.ForeignKey(Profile,blank=True,null=True)
    commentator = models.CharField(max_length=30,blank=True,null=True)    
    cpyrght = models.CharField(max_length=30, default='buckanjaren',blank=True,null=True)
    slug = models.SlugField(max_length=40, unique=True)
    site = models.ForeignKey(Site,blank=True,null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Tag,blank=True)
    media = models.ManyToManyField(Media,null=True)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.published_date.year, self.published_date.month, self.slug)

    def __str__(self):
        return self.title    
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ["-published_date"]

    