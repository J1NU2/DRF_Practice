from django.db import models
from django.utils import timezone


# Create your models here.
# 제품 모델
class Product(models.Model):
    # 작성자 / 제목 / 썸네일 / 설명 / 등록일자 / 노출시작일 / 노출종료일
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    # upload_to='img/product_img/%Y%m%d'
    thumbnail = models.ImageField("썸네일", upload_to='product/img/%Y%m%d', width_field=None, height_field=None, max_length=100)
    description = models.TextField("설명")
    created_at = models.DateTimeField("등록일자", auto_now_add=True)
    show_date_start = models.DateTimeField("노출 시작 일자", default=timezone.now)
    show_date_end = models.DateTimeField("노출 종료 일자", default=timezone.now)

    # 추가 : 가격 / 수정일자 / 활성화여부
    price = models.IntegerField("가격", default=0)
    update_at = models.DateTimeField("수정일자", auto_now=True)
    is_active = models.BooleanField("활성화 여부", default=True)

    def __str__(self):
        return f'{self.user.username}님이 등록한 {self.title}입니다.'


USER_RATING = {
    (1, "1점"),
    (2, "2점"),
    (3, "3점"),
    (4, "4점"),
    (5, "5점"),    
}


# 리뷰 모델
class Review(models.Model):
    # 작성자 / 상품 / 내용 / 평점 / 작성일
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="상품", on_delete=models.CASCADE)
    content = models.TextField("내용")
    rating = models.IntegerField("평점", choices=USER_RATING, default=1)
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}님이 {self.product.title} 제품에 대해 남긴 리뷰입니다.'
