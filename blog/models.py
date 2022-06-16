from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField("이름", max_length=20)
    explanation = models.TextField("설명")

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    category = models.ManyToManyField(to=Category, verbose_name="카테고리")
    content = models.TextField("내용")

    def __str__(self):
        return f'{self.user.username}님의 글입니다. : {self.title}'
