# 序列化

rest 序列化由`rest_framework.serializers`完成  

<!-- more -->

## 最原始的写法

```py
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField()  # row.title
    id = serializers.IntegerField()  # row.id
    status = serializers.CharField(source='get_status_display')  # row.get_status_display()
```

rest 重写了`django.models`中的这些字段类型名，可以向定义模型一样定义哪写字段需要被序列化以及被序列化成什么样，字段名需要和models中的字段名一一对应，在`view`中

```py
def get(self, request, *args, **kwargs):
    """
    获取文章列表，每页10个，分页
    """
    articles_list = Article.objects.all()
    articles_list_ser = ArticleSerializer(instance=articles_list, many=True)
    return JsonResponse(articles_list_ser.data, safe=False)
```

`instance`参数指定从数据库中拿到的需要序列化的数据集合  
`many`申明有多条数据需要序列化，这多条数据就会以`[]`的形式展示  
最后`.data`就是序列化后的json数据

这就是序列化后的结果

```json
[
  {
    "title": "Django搭建前后端分离的个人博客",
    "id": 1,
    "status": "已读"
  }
]
```

如果指定了`source`字段，则序列化中的字段名可以不与`model`中的字段名一一对应，如果`model`中是`choise`字段，使用`get_xxx_display`可以获得对应的值。

### 自定义字段

```py
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField()
    id = serializers.IntegerField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, row):
        tags = row.tags.all()
        result = []
        for tag in tags:
            result.append({'id': tag.id, 'name': tag.name})
        return result
```

结果

```json
[
  {
    "title": "Django搭建前后端分离的个人博客",
    "id": 1,
    "tags": [
      {
        "id": 2,
        "name": "django"
      },
    ]
  }
]
```

对于`ManytoMany`的字段，我们可以使用`SerializerMethodField()`自定义,然后加一个`get_xxx`的成员函数，函数返回值会作为序列化后的结果

## ModelSerializer

`ModelSerializer`是继承自`Serializer`的，使用它可以简化上面的步骤

```py
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
```

这样就会序列化表中所有数据

也可以自定义字段，如

```py
class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()

    def get_tags(self, row):
        tags = row.tags.all()
        result = []
        for tag in tags:
            result.append({'id': tag.id, 'name': tag.name})
        return result

    def get_create_time(self, row):
        return row.create_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Article
        fields = ['id', 'title', 'create_time', 'abstract', 'tags']
```

## 深度控制

可以使用`depth`控制连接表的深度，如：

```py
class ArticleSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    def get_create_time(self, row):
        return row.create_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Article
        fields = ['id', 'title', 'create_time', 'abstract', 'tags']
        depth = 1
```

rest会自动连接表，实现和上面一样的操作，深度应该控制在10层以内。

## HyperlinkedIdentityField

可以直接反向生成url

```py
class ArticleSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()
    detail = serializers.HyperlinkedIdentityField(view_name='detail', source='id')

        class Meta:
        model = Article
        fields = ['id', 'title', 'create_time', 'abstract', 'tags', 'detail']
        depth = 1
```

```py
urlpatterns = [
    path('', ArticlesListView.as_view()),
    url(r'detail/(?P<pk>\d+)$', DetailView.as_view(), name='detail')
]
```

```py
class ArticlesListView(APIView):

    def get(self, request, *args, **kwargs):
        pagination = PageNumberPagination()
        articles_list = Article.objects.all()
        articles_list_ser = ArticleSerializer(instance=articles_list, context={'request': request}, many=True)
        return JsonResponse(articles_list_ser.data, safe=False)
```

结果

```json
[
  {
    "id": 1,
    "title": "Django搭建前后端分离的个人博客",
    "create_time": "2020-01-26 10:15:50",
    "abstract": "Django搭建前后端分离的个人博客",
    "tags": [
      {
        "id": 2,
        "name": "django"
      },
    ],
    "detail": "http://127.0.0.1:8000/detail/1"
  }
]
```

1. 如果要使用HyperlinkedIdentityField，需要在实例化`YourSerializer`时添加`context={'request': request}`
2. url中的`pk`是默认值，如果要修改，请使用`lookup_url_kwarg="detail"`, 如

```py
detail = serializers.HyperlinkedIdentityField(view_name='detail', source='id', lookup_url_kwarg="detail")
url(r'detail/(?P<detail>\d+)$', DetailView.as_view(), name='detail')
```

3. `sourse`指定以什么拼接新url，默认是`pk`也就是序号

## 源码流程

在`view`中执行` articles_list_ser = ArticleSerializer(instance=articles_list, context={'request': request}, many=True)`时，就是在实例化一个`ArticleSerializer`对象，而`ArticleSerializer`继承自`serializers.ModelSerializer`,且没有自己的`__new__()`和`__init__()`方法，就会使用父类的，但`serializers.ModelSerializer`也没有，继续往上找，`serializers.ModelSerializer`继承自`Serializer`，也没有，再往上`Serializer`继承自`BaseSerializer`
在`BaseSerializer`中有`__new__()`和`__init__()`,先执行`__new__()`

```py
    def __new__(cls, *args, **kwargs):
        if kwargs.pop('many', False):
            # 对QuerySet处理
            return cls.many_init(*args, **kwargs)
        # 处理对象
        return super(BaseSerializer, cls).__new__(cls, *args, **kwargs)
```

`__new__()`返回的就是对象，`__init__()`负责进一步加工这个对象（初始化），在`__new__()`中，根据`many`的值的不同，返回不同的对象，如果`many=False`,也就是要序列化的只时一个对象，就返回自己（`BaseSerializer`）对象，否则也就是要处理的是多条数据（`QuerySet`），就调用`many_init()`

```py
@classmethod
def many_init(cls, *args, **kwargs):
    allow_empty = kwargs.pop('allow_empty', None)
    child_serializer = cls(*args, **kwargs)
    list_kwargs = {
        'child': child_serializer,
    }
    if allow_empty is not None:
        list_kwargs['allow_empty'] = allow_empty
    list_kwargs.update({
        key: value for key, value in kwargs.items()
        if key in LIST_SERIALIZER_KWARGS
    })
    meta = getattr(cls, 'Meta', None)
    list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
    return list_serializer_class(*args, **list_kwargs)
```

`many_init()`先从`Meta`中找有没有指定`list_serializer_class`,没有就使用`ListSerializer`然后返回`list_serializer_class`对象  
也就是在默认不指定`list_serializer_class`的情况下，处理对象使用`BaseSerializer`处理QuerySet使用`ListSerializer`

最后，各自执行各自的`__init__()`方法完成初始化操作，实例化对象完成

然后我们调用了实例化出来的对象的`data`属性

```py
@property
def data(self):
    ret = super(Serializer, self).data
    return ReturnDict(ret, serializer=self)
```

然后执行其父类的`data`属性方法

```py
@property
def data(self):
    if not hasattr(self, '_data'):
        if self.instance is not None and not getattr(self, '_errors', None):
            self._data = self.to_representation(self.instance)
        elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
            self._data = self.to_representation(self.validated_data)
        else:
            self._data = self.get_initial()
    return self._data
```

然后在正常情况下会执行`to_representation()`

```py
def to_representation(self, instance):
    ret = OrderedDict()
    fields = self._readable_fields

    for field in fields:
        try:
            attribute = field.get_attribute(instance)
        except SkipField:
            continue
        check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
        if check_for_none is None:
            ret[field.field_name] = None
        else:
            ret[field.field_name] = field.to_representation(attribute)

    return ret
```

然后执行`get_attribute()`方法

```py
def get_attribute(self, instance):
    try:
        return get_attribute(instance, self.source_attrs)
    except (KeyError, AttributeError) as exc:
        pass
```

会在执行`get_attribute()`方法。但携带`instance, self.source_attrs`,前者就是从数据库拿出来的数据，后者是一个列表，就是根据我们的`source`参数按`.`分割后的结果

```py
if self.source == '*':
    self.source_attrs = []
else:
    self.source_attrs = self.source.split('.')
```

```py
def get_attribute(instance, attrs):
    for attr in attrs:
        try:
            if isinstance(instance, Mapping):
                instance = instance[attr]
            else:
                instance = getattr(instance, attr)
        except ObjectDoesNotExist:
            return None
        if is_simple_callable(instance):
            try:
                instance = instance()
            except (AttributeError, KeyError) as exc:
                raise ValueError('Exception raised in callable attribute "{0}"; original exception was: {1}'.format(attr, exc))

    return instance
```

instance是从数据库中拿出来的结果集，循环attrs列表，从`instance`中拿到这些值，如果可调用，就返回它执行后的结果

## 请求数据校验