from django.db import models


# Create your models here.
# 카테고리 모델
class Category(models.Model):
    name = models.CharField("이름", max_length=20)
    explanation = models.TextField("설명")

    def __str__(self):
        return self.name


# 아티클(게시글) 모델
class Article(models.Model):
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    category = models.ManyToManyField(to=Category, verbose_name="카테고리")
    content = models.TextField("내용", null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}님의 글입니다. : {self.title}'


# 댓글 모델
class Comment(models.Model):
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, verbose_name="게시글", on_delete=models.CASCADE)
    comment = models.TextField("댓글", null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}님의 {self.article.title} 게시글에 대한 댓글입니다.'
