from django.test import TestCase
# chap36 test
# Create your tests here.
import datetime
from django.utils import timezone
from article.models import ArticlePost
from django.contrib.auth.models import User
from time import sleep
from django.urls import reverse
class ArticlePostModelTests(TestCase):
    def test_was_created_recently_with_future_article(self):
        # 若文章创建时间为未来，返回 False
        author = User(username='user', password='test_password')
        author.save()
        future_article = ArticlePost(
            author=author,
            title='test',
            body='test',
            created=timezone.now() + datetime.timedelta(days=30)
            )
        self.assertIs(future_article.was_created_recently(), False)
# 基本就是把刚才在Shell中的测试代码抄了过来。有点不同的是末尾这个assertIs方法，
# 了解**“断言”**的同学会对它很熟悉：它的作用是检测方法内的两个参数是否完全一致，如果不是则抛出异常，提醒你这个地方是有问题滴。

class ArtitclePostViewTests(TestCase):
    def test_increase_views(self):
        # 请求详情视图时，阅读量 +1
        author = User(username='user4', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test4',
            body='test4',
            )
        article.save()
        self.assertIs(article.total_views, 0)

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)

        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(viewed_article.total_views, 1)

    def test_increase_views_but_not_change_updated_field(self):
        # 请求详情视图时，不改变 updated 字段
        author = User(username='user5', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test5',
            body='test5',
        )
        article.save()

        sleep(0.5)

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)

        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(viewed_article.updated - viewed_article.created < timezone.timedelta(seconds=0.1), True)