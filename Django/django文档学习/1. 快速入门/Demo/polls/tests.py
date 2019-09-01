from django.test import TestCase
import datetime
from .models import Question
from django.utils import timezone
from django.shortcuts import reverse

# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future(self):
        time = timezone.now() + datetime.timedelta(days=30)
        test_question = Question(pub_date=time)
        self.assertIs(test_question.was_published_recently(), False)
    
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# 测试index

def creat_question(question_text: str, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewText(TestCase):
    def test_no_question(self):
        """
        测试数据库中没有数据的情况，页面应该包含 “没有任何投票” 字样
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "没有任何投票".encode('utf-8'))
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        """
        测试过去时间的投票能否显式在index页面，响应应为200，页面中应该包含测试
        标题名称test_question_text
        """
        creat_question('test_question_text_past', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], [
                                 '<Question: test_question_text_past>'])

    def test_future_question(self):
        """
        测试发布时间是 "未来" 的投票能否显式在index中，期望响应200，
        context['question_list']为空,因为每次测试数据库会被重置，所以页面期望出现
        “没有任何投票”字样
        """
        creat_question('test_question_text_future', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "没有任何投票".encode('utf-8'))
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_future_question_and_past_question(self):
        """
        测试一个未来发布一个过去发布的投票情况，未来发布的不应该展示在index页面
        """
        creat_question('test_question_text_future', days = 30)
        creat_question('test_question_text_past', days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['question_list'], [
                                 '<Question: test_question_text_past>'])

    def test_two_past_questions(self):
        """
        测试两个过去发布的投票能否都展示在index页面
        """
        creat_question('test_question_text_past1', days = -30)
        creat_question('test_question_text_past2', days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['question_list'], [
                                 '<Question: test_question_text_past2>', '<Question: test_question_text_past1>'])


class QuestionDetailViewText(TestCase):
    def test_future_detail_question(self):
        """
        测试将在未来发布的投票能否在detail页访问到
        """
        question = creat_question('test_question_text_future', days=30)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEquals(response.status_code, 404)




