from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.models import FlatPage
from buc.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.published_date

class FlatpageSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5
    def items(self):
        return FlatPage.objects.all()
