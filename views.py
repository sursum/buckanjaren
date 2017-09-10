from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.generic import ListView, DetailView
from buc.models import Category, Article, Tag

# Create your views here.
class HomeView(ListView):
    template_name = "buc/homeview.html"
    article = Article()
    title = "HomeView"
 
    def mainfeature(self): 
        featuerArticle = Article.objects.filter(tags__name='Feature').latest('published_date')                
        return featuerArticle
        
    def minitrue(self):
        return Article.objects.all()[:10]

    def published_media(self):
        return Article.objects.all()[:10]

    def getlatestopinion(self):
        return Article.objects.filter(tags__name='Opinion')[:3]

    def category_pol(self):
        # Politik, Ekonomi, Kultur, E-Sport, Vetenskap, Hälsa, Världen
        print (Article.objects.filter(category__name='Politik') )
        try:
            return Article.objects.filter(category__name='Politik') 
        except Category.DoesNotExist:
            return Article.objects.none()

    def category_ekon(self):
        # Politik, Ekonomi, Kultur, E-Sport, Vetenskap, Hälsa, Världen
        try:
            return Article.objects.filter(category__name='Ekonomi') 
        except Category.DoesNotExist:
            return Article.objects.none()

    def category_kult(self):
        # Politik, Ekonomi, Kultur, E-Sport, Vetenskap, Hälsa, Världen
        try:
            return Article.objects.filter(category__name='Kultur') 
        except Category.DoesNotExist:
            return Article.objects.none()

    def category_esport(self):
        # Politik, Ekonomi, Kultur, E-Sport, Vetenskap, Hälsa, Världen
        try:
            return Article.objects.filter(category__name='E-Sport') 
        except Category.DoesNotExist:
            return Article.objects.none()

    def category_vet(self):
        # Politik, Ekonomi, Kultur, E-Sport, Vetenskap, Hälsa, Världen
        try:
            return Article.objects.filter(category__name='Vetenskap') 
        except Category.DoesNotExist:
            return Article.objects.none()

    
    def category_halsa(self):
        # Politik, Ekonomi, Kultur, E-Sport, Vetenskap, Hälsa, Världen
        try:
            return Article.objects.filter(category__name='Hälsa') 
        except Category.DoesNotExist:
            return Article.objects.none()


    def dockyard(self):
        try:
            return Article.objects.filter(tags__name='pirate-code') 
        except Tag.DoesNotExist:
            return Article.objects.none()
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
            return tag.article_set.all()
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
