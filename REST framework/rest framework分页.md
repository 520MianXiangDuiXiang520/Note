```py
from rest_framework.pagination import CursorPagination, PageNumberPagination, LimitOffsetPagination
from rest_framework.settings import api_settings


class MyCursorPagination(CursorPagination):
    """
    只能看这一页和上一页
    """
    cursor_query_param = 'cursor'
    ordering = '-id'
    page_size_query_param = None
    max_page_size = None


class MyPageNumberPagination(PageNumberPagination):
    page_size = api_settings.PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = None
    max_page_size = None
    last_page_strings = ('last',)

  
class MyLimitOffsetPagination(LimitOffsetPagination):
    """
    从第几个看后面的
    """
    default_limit = api_settings.PAGE_SIZE
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None

```

```py
    def get(self, request, *args, **kwargs):
        """
        获取文章列表，每页10个，分页
        """
        pagination = PageNumberPagination()
        articles_list = Article.objects.all()
        pg_articles = pagination.paginate_queryset(queryset=articles_list, request=request, view=self)
        articles_list_ser = ArticleSerializer(instance=pg_articles, context={'request': request}, many=True)
        return pagination.get_paginated_response(articles_list_ser.data)
```