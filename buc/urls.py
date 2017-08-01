from django.views.generic import HomeView, DetailView
from buc.views import CategoryListView

from buc.models import Article

urlpatterns = patterns[]'',
    # Index
    url('^$', HomeView.as_view(
        model=Article,
        )),

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

        )),

    # Tags
    url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
        paginate_by=5,
        model=Tag,
        )),

    # Search posts
    url(r'^search', 'buc.views.getSearchResults'),
]
