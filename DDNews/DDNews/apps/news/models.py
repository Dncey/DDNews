
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表

class User(AbstractUser):
    """
    用户表
    """
    GENDER_CHOICES = (
        (1, "男"),
        (2, "女"),
    )

    avatar_url = models.CharField(max_length=256, verbose_name='用户头像路径')
    mobile = models.CharField(max_length=11, null=False, unique=True, verbose_name='用户手机号')
    signature = models.CharField(max_length=50, null=True, verbose_name='用户签名')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='用户性别')
    email_active = models.BooleanField(default=False, verbose_name='用户邮箱绑定状态')
    # 多对多收藏关系  related为关联的另一张表反向查询自己的字段
    collect_new = models.ManyToManyField('News', through='User_Collection', through_fields=('user', 'new'),
                                         related_name='collected_user')



    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户user'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.username)


# Create your models here.


class User_Fans(models.Model):
    """
    用户关注表
    """
    follow = models.ForeignKey(User, verbose_name='关注', on_delete=models.CASCADE, related_name='follows')
    fan = models.ForeignKey(User, verbose_name='粉丝', on_delete=models.CASCADE, related_name='fans')

    class Meta:
        db_table = 'tb_user_fans'
        verbose_name = '用户关注表'
        verbose_name_plural = verbose_name




class NewsCategory(BaseModel):
    """
    新闻分类表
    """
    name = models.CharField(max_length=64, null=False, verbose_name='新闻分类')

    class Meta:
        db_table = 'tb_news_category'
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class News(BaseModel):
    """
    新闻表
    """

    NEWS_STATUS_CHOICES = (
        (0, "审核通过"),
        (1, "审核中"),
        (2, "审核不通过"),
    )

    title = models.CharField(max_length=256, null=False, verbose_name='新闻标题')
    source = models.CharField(max_length=64, null=False)
    index_image_url = models.CharField(max_length=256,null=True,verbose_name='新闻索引图片路径')
    index_image_url_list = models.CharField(max_length=256,verbose_name='新闻索引图片路径',null=True)
    
    # 用户上传数据则为新闻内容的前一段,后端处理
    digest = models.CharField(max_length=256, null=True, verbose_name='新闻简要')
    content = models.TextField(null=False, verbose_name='新闻内容')
    clicks = models.IntegerField(default=0, verbose_name='文章点击数')
    status = models.SmallIntegerField(choices=NEWS_STATUS_CHOICES, default=0, verbose_name='文章审核状态')
    reason = models.CharField(max_length=256, verbose_name='审核不通过原因')  # 未通过原因，status = 2 的时候使用
    report_time = models.DateTimeField(verbose_name='发布时间')
    # 新闻关键字 通过jieba进行分词
    digest_label = models.CharField(max_length=256, verbose_name='新闻关键字')
    is_spider = models.BooleanField(default=True,verbose_name='是否是爬取的新闻')
    source_avatar_url = models.CharField(max_length=256,default='null',verbose_name='来源用户的头像')

    # 外键--------------------------
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者id', default='1')  # 爬取的默认为管理员id=1
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT, verbose_name='新闻分类')


    class Meta:
        db_table = 'tb_news'
        verbose_name = '新闻表'
        verbose_name_plural = verbose_name


def __str__(self):
    return '%s: %s' % (self.id, self.title)

class User_Collection(models.Model):
    """
    用户收藏表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
    new = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='新闻id')
    is_delete = models.BooleanField(default=False, verbose_name='标记是否删除')
    class Meta:
        db_table = 'tb_user_collection'
        verbose_name = '用户收藏表'
        verbose_name_plural = verbose_name




class Comment(BaseModel):
    """
    评论信息表
    """
    user = models.ForeignKey(User, verbose_name='评论者')
    new = models.ForeignKey(News, verbose_name='评论的新闻')
    content = models.CharField(max_length=200, null=False, verbose_name='评论内容')
    like = models.IntegerField(default=0, verbose_name='点赞数')
    # 评论信息的举报
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    #父评论信息
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,verbose_name='父评论的id')

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.content)


class Comment_report(BaseModel):
    """评论信息举报"""
    user = models.ForeignKey(User, verbose_name='举报用户')
    comment = models.ForeignKey(Comment, verbose_name='评论id')
    reason = models.CharField(max_length=200, null=False, verbose_name='举报原因')

    class Meta:
        db_table = 'Comment_report'
        verbose_name = '评论举报表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.content)


class Slide_image(models.Model):
    """
    广告轮播图表
    """
    new = models.ForeignKey(News,verbose_name='轮播的新闻id')
    title = models.CharField(max_length=30, null=False, verbose_name='轮播图标题')
    url = models.CharField(max_length=128,verbose_name="轮播图图片url")
    is_recommend =models.BooleanField(default=False,verbose_name='图片是否显示')

    class Meta:
        db_table = 'tb_slide_show'
        verbose_name = '轮播广告表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.title)

class Search_keywords(models.Model):
    """
    搜索关键字表
    """
    key_wrods = models.CharField(max_length=128,verbose_name='搜索关键字')
    search_times = models.IntegerField(verbose_name='搜索次数')

    class Meta:
        db_table = 'tb_search_keywords'
        verbose_name = ' 搜索关键字表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.key_wrods)