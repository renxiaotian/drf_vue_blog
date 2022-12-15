from article.serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from article.models import Article
from article.serializers import ArticleDetailSerializer
from rest_framework import mixins
from rest_framework import generics
#from rest_framework.permissions import IsAdminUser
from article.permissions import IsAdminUserOrReadOnly
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  filters
from article.models import Category
from article.serializers import CategorySerializer
from article.serializers import CategorySerializer, CategoryDetailSerializer
from article.models import Tag
from article.serializers import TagSerializer
from article.models import Avatar
# 这个 AvatarSerializer 最后来写
from article.serializers import AvatarSerializer

# 视图集类把前面章节写的列表、详情等逻辑都集成到一起，并且提供了默认的增删改查的实现。这些基础逻辑都在父类 ModelViewSet 里封装实现了，有兴趣可耐心研究源码。
class ArticleViewSet(viewsets.ModelViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['author__username', 'title']
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    # 如果要实现更常用的模糊匹配，就可以使用SearchFilter做搜索后端：非常轻松就实现了对文章标题的检索。
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        #perform_create()跟之前一样，在创建文章前，提供了视图集无法自行推断的用户外键字段。

    # 这些渲染后的数据，在文章详情接口是需要的，但是在列表接口却没太有必要，因此又要用到视图集根据请求方式动态获取序列化器的技术了：序列化器 ArticleDetailSerializer 还没有写，这就来搞定它。
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None
    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
