from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.generic import ListView, DetailView
from buc.models import Category, Article, Tag

# Create your views here.
class HomeView(ListView):
    template_name = "buc/homeview.html"
    article = Article()
    title ="HomeView"

    def mainfeature(self):        
        return Article.objects.all()

    def minitrue(self):
        return
    def latest_news(self):
        return
    def carousel_features(self):
        return
    def category_news(self):
        return
    def dockyard(self):
        return

#class ArticleView(DetailView):
     #   return

class CategoryListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Article.objects.filter(category=category)
        except Category.DoesNotExist:
            return Article.objects.none()

class TagListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Article.objects.none()

def getSearchResults(request):
    """
    Search for an article by title or text
    """
    # Get the query data
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    # Query the database
    if query:
        results = Article.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
    else:
        results = None

    # Add pagination
    pages = Paginator(results, 5)

    # Get specified page
    try:
        returned_page = pages.page(page)
    except EmptyPage:
        returned_page = pages.page(pages.num_pages)

    # Display the search results
    return render_to_response('buc/search_post_list.html',
                              {'page_obj': returned_page,
                               'object_list': returned_page.object_list,
                               'search': query})
