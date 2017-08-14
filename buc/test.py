
from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from buc.models import Article, Category, Tag
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import factory.django
import markdown
#import markdown2 as markdown
#import feedparser



class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site
        django_get_or_create = (
            'name',
            'domain'
        )
        
    name = 'example.com'
    domain = 'example.com'

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username','email', 'password',)

    username = 'testuser'
    email = 'user@example.com'
    password = 'testuser'


class FlatPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FlatPage
        django_get_or_create = (
            'url',
            'title',
            'content'
        )

    url = '/about/'
    title = 'About me'
    content = 'All about me'


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        django_get_or_create = (
            'title',
            'text',
            'slug',
            'published_date'
        )

    title = 'My first article'
    text = 'This is my first blog article'
    slug = 'my-first-article'
    published_date = timezone.now()
    site = factory.SubFactory(SiteFactory)
    category = factory.SubFactory(CategoryFactory)

###########################################################################
# Create your tests here.
###########################################################################
class ArticleTest(TestCase):
    def test_create_article(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        ''' site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save() '''

        # Create the article
        article = Article()

         # Set the attributes
        article.title = 'My first article'
        article.text = 'This is my first article'
        article.published_date = timezone.now()
        ## article.created_date = timezone.now() Set by default
        article.comment = 'This is a comment'
        ## article.cpyrght = 'buckanjaren' Set by default

        ## Left to do
        ''' 
        article.editor = models.ForeignKey(User,blank=True,null=True)
        article.creator = models.ForeignKey(Profile,blank=True,null=True)
        article.commentator = models.ForeignKey(Profile,blank=True,null=True)
        '''

        # Save it
        article.save()

         # Check we can find it
        all_articles = Article.objects.all()
        self.assertEquals(len(all_articles), 1)
        only_article = all_articles[0]
        self.assertEquals(only_article, article)

         # Check attributes
        self.assertEquals(only_article.title, 'My first article')
        self.assertEquals(only_article.text, 'This is my first article')
        self.assertEquals(only_article.published_date.day, article.published_date.day)
        self.assertEquals(only_article.published_date.month, article.published_date.month)
        self.assertEquals(only_article.published_date.year, article.published_date.year)
        self.assertEquals(only_article.published_date.hour, article.published_date.hour)
        self.assertEquals(only_article.published_date.minute, article.published_date.minute)
        self.assertEquals(only_article.published_date.second, article.published_date.second)

        
        self.assertEquals(only_article.created_date.day, article.created_date.day)
        self.assertEquals(only_article.created_date.month, article.created_date.month)
        self.assertEquals(only_article.created_date.year, article.created_date.year)
        self.assertEquals(only_article.created_date.hour, article.created_date.hour)
        self.assertEquals(only_article.created_date.minute, article.created_date.minute)
        self.assertEquals(only_article.comment, 'This is a comment')
        self.assertEquals(only_article.cpyrght, 'buckanjaren')
        
###########################################################################
###########################################################################
class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/', follow=True)

        # Check response code
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content.decode('utf-8'))

        # Log the user in
        self.client.login(username='bobsmith', password="testuser")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content.decode('utf-8'))

    def test_logout(self):
        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content.decode('utf-8'))

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content.decode('utf-8'))

    def test_create_category(self):
        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Check response code
        response = self.client.get('/admin/buc/category/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/buc/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = CategoryFactory()

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Edit the category
        response = self.client.post('/admin/buc/category/' + str(category.pk) + '/change/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content.decode('utf-8'))

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEqual(only_category.name, 'perl')
        self.assertEqual(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = CategoryFactory()

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Delete the category
        response = self.client.post('/admin/buc/category/' + str(category.pk) + '/delete/', {
            'article': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content.decode('utf-8'))

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 0)

    def test_create_tag(self):
        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Check response code
        response = self.client.get('/admin/buc/tag/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new tag
        response = self.client.post('/admin/buc/tag/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new tag now in database
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 1)

    def test_edit_tag(self):
        # Create the tag
        tag = TagFactory()

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Edit the tag
        response = self.client.post('/admin/buc/tag/' + str(tag.pk) + '/change/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content.decode('utf-8'))

        # Check tag amended
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEqual(only_tag.name, 'perl')
        self.assertEqual(only_tag.description, 'The Perl programming language')

    def test_delete_tag(self):
        # Create the tag
        tag = TagFactory()

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Delete the tag
        response = self.client.post('/admin/buc/tag/' + str(tag.pk) + '/delete/', {
            'article': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content.decode('utf-8'))

        # Check tag deleted
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 0)

    def test_create_article(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Check response code
        response = self.client.get('/admin/buc/article/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new article
        response = self.client.post('/admin/buc/article/add/', {
            'title': 'My first article',
            'text': 'This is my first article',
            'published_date_0': '2013-12-28',
            'published_date_1': '22:00:04',
            'slug': 'my-first-article',
            'site': '1',
            'category': str(category.pk),
            'tags': str(tag.pk)
        },
        follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new article now in database
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)
    
    def test_create_article_without_tag(self):
        # Create the category
        category = CategoryFactory()

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Check response code
        response = self.client.get('/admin/buc/article/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new article
        response = self.client.post('/admin/buc/article/add/', {
            'title': 'My first article',
            'text': 'This is my first article',
            'published_date_0': '2013-12-28',
            'published_date_1': '22:00:04',
            'slug': 'my-first-article',
            'site': '1',
            'category': str(category.pk)
        },
        follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully        
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new article now in database
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)

    def test_edit_article(self):
        # Create the article
        article = ArticleFactory()

        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()
        article.tags.add(tag)

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Edit the article
        response = self.client.post('/admin/buc/article/' + str(article.pk) + '/change/', {
            'title': 'My second article',
            'text': 'This is my second blog article',
            'published_date_0': '2013-12-28',
            'published_date_1': '22:00:04',
            'slug': 'my-second-article',
            'site': '1',
            'category': str(category.pk),
            'tags': str(tag.pk)
        },
        follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content.decode('utf-8'))

        # Check article amended
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)
        only_article = all_articles[0]
        self.assertEqual(only_article.title, 'My second article')
        self.assertEqual(only_article.text, 'This is my second blog article')

    def test_delete_article(self):
        # Create the article
        article = ArticleFactory()

        # Create the tag
        tag = TagFactory()
        article.tags.add(tag)

        # Check new article saved
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)

        # Log in
        self.client.login(username='bobsmith', password="testuser")

        # Delete the article
        response = self.client.post('/admin/buc/article/' + str(article.pk) + '/delete/', {
            'article': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content.decode('utf-8'))

        # Check article deleted
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 0)

###########################################################################
## Test of Article View
###########################################################################
class ArticleViewTest(BaseAcceptanceTest):

    def setUp(self):

        self.client = Client()

    def test_index(self):
        # Create the article
        article = ArticleFactory(text='This is [my first blog article](http://127.0.0.1:8000/)')

        # Create the tag
        tag = TagFactory(name='perl', description='The Perl programming language')
        article.tags.add(tag)

        # Check new article saved
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)

        # Fetch the index
        response = self.client.get(reverse('buc:HomeView'))
        self.assertEqual(response.status_code, 200)

        # Check the article title is in the response
        self.assertTrue(article.title in response.content.decode('utf-8'))

        # Check the article text is in the response        
        self.assertTrue(markdown.markdown(article.text) in response.content.decode('utf-8'))

        # Check the article category is in the response
        self.assertTrue(article.category.name in response.content.decode('utf-8'))

        # Check the article tag is in the response
        article_tag = all_articles[0].tags.all()[0]
        #print(response.content.decode('utf-8'))
        self.assertTrue(article_tag.name in response.content.decode('utf-8'))

        # Check the article date is in the response
        self.assertTrue(str(article.published_date.year) in response.content.decode('utf-8'))        
        self.assertTrue(article.published_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(article.published_date.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog article</a>' in response.content.decode('utf-8'))

        # Check the correct template was used
        self.assertTemplateUsed(response, 'buc/homeview.html')

    def test_article_page(self):
        # Create the article
        article = ArticleFactory(text='This is [my first blog article](http://127.0.0.1:8000/)')

        # Create the tag
        tag = TagFactory(name='perl', description='The Perl programming language')
        article.tags.add(tag)

        # Check new article saved
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)
        only_article = all_articles[0]
        self.assertEqual(only_article, article)

        # Get the article URL
        article_url = only_article.get_absolute_url()    
        

        # Fetch the article
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 200)

        # Check the article title is in the response
        self.assertTrue(article.title in response.content.decode('utf-8'))

        # Check the article category is in the response        
        self.assertTrue(article.category.name in response.content.decode('utf-8'))

        # Check the article tag is in the response
        article_tag = all_articles[0].tags.all()[0]
        self.assertTrue(article_tag.name in response.content.decode('utf-8'))

        # Check the article text is in the response
        self.assertTrue(markdown.markdown(article.text) in response.content.decode('utf-8'))

        # Check the article date is in the response
        self.assertTrue(str(article.published_date.year) in response.content.decode('utf-8'))
        self.assertTrue(article.published_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(article.published_date.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog article</a>' in response.content.decode('utf-8'))

        # Check the correct template was used
        self.assertTemplateUsed(response, 'buc/article_detail.html')

    def test_category_page(self):
        # Create the article
        article = ArticleFactory(text='This is [my first blog article](http://127.0.0.1:8000/)')

        # Check new article saved
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)
        only_article = all_articles[0]
        self.assertEqual(only_article, article)

        # Get the category URL
        category_url = article.category.get_absolute_url()

        # Fetch the category
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)

        # Check the category name is in the response
        self.assertTrue(article.category.name in response.content.decode('utf-8'))

        # Check the article text is in the response
        self.assertTrue(markdown.markdown(article.text) in response.content.decode('utf-8'))

        # Check the article date is in the response
        self.assertTrue(str(article.published_date.year) in response.content.decode('utf-8'))
        self.assertTrue(article.published_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(article.published_date.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog article</a>' in response.content.decode('utf-8'))

        # Check the correct template was used
        self.assertTemplateUsed(response, 'buc/article_list.html')

    def test_nonexistent_category_page(self):
        category_url = '/category/blah/'
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No articles found' in response.content.decode('utf-8'))

    def test_tag_page(self):
        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the article
        article = ArticleFactory(text='This is [my first blog article](http://127.0.0.1:8000/)')

        # Create the tag
        tag = TagFactory()
        article.tags.add(tag)

        # Check new article saved
        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 1)
        only_article = all_articles[0]
        self.assertEqual(only_article, article)

        # Get the tag URL
        tag_url = article.tags.all()[0].get_absolute_url()

        # Fetch the tag
        response = self.client.get(tag_url)
    
        self.assertEqual(response.status_code, 200)

        # Check the tag name is in the response
        self.assertTrue(article.tags.all()[0].name in response.content.decode('utf-8'))

        # Check the article text is in the response
        self.assertTrue(markdown.markdown(article.text) in response.content.decode('utf-8'))

        # Check the article date is in the response
        self.assertTrue(str(article.published_date.year) in response.content.decode('utf-8'))
        self.assertTrue(article.published_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(article.published_date.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog article</a>' in response.content.decode('utf-8'))

        # Check the correct template was used
        self.assertTemplateUsed(response, 'buc/article_list.html')

    def test_nonexistent_tag_page(self):
        tag_url = '/tag/blah/'
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No articles found' in response.content.decode('utf-8'))

    