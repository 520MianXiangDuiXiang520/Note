from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
# 通用视图模块
from django.views import generic
from django.utils import timezone

# Create your views here.

class IndexViews(generic.ListView):
    """
    用来渲染一个列表视图
    """
    model = Question
    context_object_name = 'question_list'
    template_name = 'polls/index.html'
    
    # 必须实现这个方法，来约束渲染哪写数据
    def get_queryset(self):
        # pub_date__lte pub_date比当前时间早的
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailViews(generic.DetailView):
    model = Question
    # 声明上下文（render中的那个字典）名
    context_object_name = 'question'
    # 声明作用的模板名
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        只允许查看之前已经发布的
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultViews(generic.DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'polls/result.html'



def vote(request, question_id):
    # 找不到抛出404页面
    question = get_object_or_404(klass=Question, pk=question_id)
    
    choice_list = Choice.objects.filter(question=question)
    
    if request.method == 'POST':
        try:
            get_choice_id = request.POST['choice']
            
        except KeyError:
            context = {
                'error': '请至少选择一项',
                'question': question,
                'choices': choice_list
            }
            return render(request, 'polls/detail.html', context)
        else:
            choice = get_object_or_404(Choice, id=get_choice_id)
            choice.votes += 1
            choice.save()
    
    # 重定向到直到页面，reverse用来构造url，返回str
    return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

