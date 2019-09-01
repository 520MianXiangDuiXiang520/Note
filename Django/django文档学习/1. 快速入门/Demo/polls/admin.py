from django.contrib import admin
from . models import Question, Choice

# Register your models here.


# admin.site.register(Choice)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,              {'fields': ['question_text']}),
        ('Data infomation', {'fields': ['pub_date'],
                             'classes': ['collapse']})
    ]
    inlines = [ChoiceInline]
    # 侧边栏过滤器
    list_filter = ['pub_date']
    # 搜索过滤器
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
