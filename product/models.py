from django.db import models
from django.utils import timezone


# Create your models here.
# 제품 모델
class Product(models.Model):
    # 작성자 / 제목 / 썸네일 / 설명 / 등록일자 / 노출시작일 / 노출종료일
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    # upload_to='img/product_img/%Y%m%d'
    thumbnail = models.ImageField("썸네일", upload_to='product/img/%Y%m%d', width_field=None, height_field=None, max_length=100)
    description = models.TextField("설명")
    created_at = models.DateTimeField("등록일자", auto_now_add=True)
    show_date_start = models.DateTimeField("노출 시작 일자", default=timezone.now)
    show_date_end = models.DateTimeField("노출 종료 일자", default=timezone.now)

    def __str__(self):
        return f'{self.user.username}님이 등록한 {self.title}입니다.'
