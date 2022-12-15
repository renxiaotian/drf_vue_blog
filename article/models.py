from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from markdown import Markdown

class Tag(models.Model):
    """文章标签"""
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Avatar(models.Model):
    # 标题图
    content = models.ImageField(upload_to='avatar/%Y%m%d')

# 博客文章 model
class Article(models.Model):
    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='articles')
    # 分类
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    # 标签,一篇文章可以有多个标签，一个标签可以对应多个文章，因此是多对多关系
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    # 标题图
    avatar = models.ForeignKey(Avatar, null=True, blank=True, on_delete=models.SET_NULL, related_name='article')

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc 是渲染后的目录,方法返回了包含了两个元素的元组，分别为已渲染为 html 的正文和目录。
        return md_body, md.toc

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created']




admin.site.register(Article)