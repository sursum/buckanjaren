from django.conf.urls import url
from django.views.generic import TemplateView, DetailView, ListView
from buc.models import Article, Category, Tag
from django.views.generic import ListView, DetailView
from buc.views import CategoryListView, TagListView, HomeView, getSearchResults
from django.contrib.sitemaps.views import sitemap



urlpatterns = [
    # Index
    url('^$', HomeView.as_view(
            model=Article,
            ),
            name = "HomeView"
            ),

    # # Index
    # url(r'^(?P<page>\d+)?/?$', ListView.as_view(
    #     model=Article,
    #     paginate_by=5,
    #     )),


    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Article,
        )),

    # Categories
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
        paginate_by=5,
        model=Category,
        ),
        name='category'
        ),

    # Tags
    url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
        paginate_by=5,
        model=Tag,
        ),
        name='tag'
        ),

    # Search posts
    url(r'^search', getSearchResults, name='search'),
]
