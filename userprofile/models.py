from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver


# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系(意义是一个user有一个userProfile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    #%Y%m%d是日期格式化的写法，会最终格式化为系统时间。
    # 比如说图片上传是2018年12月5日，则图片会保存在/media/avatar/2018205/中。
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


# 信号接收函数，每当新建 User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新 User 实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    '''
    post_save就是一个内置信号，它可以在模型调用save()方法后发出信号。
    有了信号之后还需要定义接收器，告诉Django应该把信号发给谁。
    装饰器receiver就起到接收器的作用。
    每当User有更新时，就发送一个信号启动post_save相关的函数。
    '''