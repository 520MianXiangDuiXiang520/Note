from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexViews.as_view(), name='index'),
    # 通用视图接受一个 pk 主键作为url的参数
    path('<int:pk>/datail/', views.DetailViews.as_view(), name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/result/', views.ResultViews.as_view(), name='result')
]
