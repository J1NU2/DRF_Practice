from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
# 카테고리 모델
class Category(models.Model):
    name = models.CharField("이름", max_length=20)
    explanation = models.TextField("설명", null=True, blank=True)

    def __str__(self):
        return self.name


# 아티클(게시글) 모델
class Article(models.Model):
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    category = models.ManyToManyField(to=Category, verbose_name="카테고리")
    content = models.TextField("내용")
    show_date_start = models.DateTimeField("노출 시작 일자", auto_now_add=True)
    show_date_end = models.DateTimeField("노출 종료 일자", default=timezone.now()+timedelta(days=7))
    # show_date_end = models.DateTimeField("노출 종료 일자", default="2022-06-21 00:00:00")

    # show_date_start = models.DateTimeField("노출 종료 일자", default="")
    # show_date_end = models.DateTimeField("노출 종료 일자", default="")

    def __str__(self):
        return f'{self.user.username}님의 글입니다. : {self.title}'


# 댓글 모델
class Comment(models.Model):
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, verbose_name="게시글", on_delete=models.CASCADE)
    comment = models.TextField("댓글")

    def __str__(self):
        return f'{self.user.username}님의 {self.article.title} 게시글에 대한 댓글입니다.'
