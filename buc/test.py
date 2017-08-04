from django.test import TestCase
from django.utils import timezone
from buc.models import Article

# Create your tests here.
class rticleTest(TestCase):
    def test_create_article(self):
        # Create the article
        article = Article()

         # Set the attributes
        article.title = 'My first article'
        article.text = 'This is my first article'
        article.pub_date = timezone.now()

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
        self.assertEquals(only_article.pub_date.day, article.pub_date.day)
        self.assertEquals(only_article.pub_date.month, article.pub_date.month)
        self.assertEquals(only_article.pub_date.year, article.pub_date.year)
        self.assertEquals(only_article.pub_date.hour, article.pub_date.hour)
        self.assertEquals(only_article.pub_date.minute, article.pub_date.minute)
        self.assertEquals(only_article.pub_date.second, article.pub_date.second)