from django.db import models
#Django具有一个简单的账号系统（User），满足一般网站的用户相关的基本功能。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
#通过reverse()方法返回文章详情页面的url，实现了路由重定向。
from django.urls import reverse
#每当你修改了models.py文件，都需要用makemigrations和migrate这两条指令迁移数据。

class ArticlePost(models.Model):
    #ArticlePost类定义了一篇文章所必须具备的要素：作者、标题、正文、创建时间以及更新时间。
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length = 100)
    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default = timezone.now)
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now = True)
    total_views = models.PositiveIntegerField(default=0)
    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # -created表示将以创建时间的倒序排列，这里的创建时间就是上面写的created，这保证最新的文章总是在网页的最上方。
        # 注意ordering是元组，括号中只含一个元素时不要忘记末尾的逗号。
        ordering = ('-created', )
    def __str__(self):
        #写一下魔术方法，方便获取标题
        return self.title
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
# Create your models here.
'''
    数据库中有各种各样的数据表，有时候几张表的数据是互相关联的。
    比如一张表记录了所有的文章，另一张表记录了所有的用户，而文章是用户发表的，
    这时候这两张表就产生了关系。外键就是用来表示这种关系的。
    而ForeignKey是用来解决“一对多”关系的。那什么又叫“一对多”？

    外键也叫FOREIGN KEY，是用于将两个表链接在一起的键。
    FOREIGN KEY是一个表中的一个字段（或字段集合），它引用另一个表中的PRIMARY KEY。
    包含外键的表称为子表，包含候选键的表称为引用表或父表。

    每个字段都是 Field 类的实例 。比如字符字段被表示为 CharField ，日期时间字段被表示为 DateTimeField。
    这将告诉Django要处理的数据类型。

    定义某些 Field 类实例需要参数。例如 CharField 需要一个 max_length参数。
    这个参数的用处不止于用来定义数据库结构，也用于验证数据。

    使用 ForeignKey定义一个关系。这将告诉 Django，每个（或多个） ArticlePost 对象都关联到一个 User 对象。
    Django具有一个简单的账号系统（User），满足一般网站的用户相关的基本功能。
    
    #Django2.0 之前的版本外键的on_delete参数可以不填；Django2.0以后on_delete是必填项。
    
    内部类class Meta提供模型的元数据。元数据是**“任何不是字段的东西”**，
    例如排序选项ordering、数据库表名db_table、单数和复数名称verbose_name和 verbose_name_plural。
    要不要写内部类是完全可选的，当然有了它可以帮助理解并规范类的行为。
    
'''

