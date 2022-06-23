from django.utils import timezone

from rest_framework import serializers

from product.models import Product as ProductModel
from product.models import Review as ReviewModel


# 제품
class ProductSerializer(serializers.ModelSerializer):
    # 해당 부분에서 오류 발생?, views.py에서 다른 코드로 실행
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.username
    
    # 조회(GET) 시 해당 user_id가 username으로 보이도록 설정
    # user = serializers.SlugRelatedField(
    #     read_only = True,
    #     slug_field = 'username'
    # )

    class Meta:
        model = ProductModel
        fields = ["user", "title", "thumbnail", "description",
        "created_at", "update_at","show_date_start", "show_date_end",
        "price", "is_active"]

    # 노출 종료 일자가 현재보다 더 이전 시점이라면 상품 등록 불가능
    def validate(self, data):
        now_date = timezone.now()

        if now_date > data.get("show_date_end"):
            raise serializers.ValidationError(
                detail = {"error": "노출 종료 일자가 현재보다 과거에 있습니다."}
            )
        return data

    # 상품 설명의 마지막에 "<등록일자>에 등록된 상품입니다." 라는 문구 추가
    def create(self, validated_data):
        product = ProductModel(**validated_data)

        create_at = product.create_at
        msg = f'{create_at}에 등록된 상품입니다.'

        product.description = product.description + msg
        product.save()

        return product

    # 상품 수정 시 상품 설명의 첫줄에 "<수정일자>에 수정되었습니다." 라는 문구 추가
    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        update_at = instance.update_at
        msg = f'{update_at}에 수정되었습니다.'

        instance.description = msg + instance.description
        instance.is_active = True
        instance.save()

        return instance

    # 공부용
    # json 데이터를 serializer를 거쳐 object로 바꾸려면 다음 단계를 거쳐야 한다.
    # validate > create OR update > 실행
    # 우선적으로 검증(validate)을 거치고 생성(create) 또는 수정(update)을 해야한다.

    # 만약 Custom validate가 있으면 우선적으로 기본 validate를 거치고 custom validate를 실행한다.
    # 하지만 Custom한 create 및 update가 있다면 Custom한 것을 실행한다.
    # def validate(self, data):
    #     if len(data.get("title")) == "":
    #         raise serializers.ValidationError(
    #             detail = {"error": "제목을 입력해주세요."}
    #         )
    #     return data

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = ReviewModel
        fields = ["user", "product", "content", "rating", "created_at"]


class ProductSecondSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    # 로그인된 사용자
    def get_user(self, obj):
        return obj.user.username

    # 평균 점수는 (리뷰 평점의 합/리뷰 갯수)로 구해주세요.
    def get_average_rating(self, obj):
        # 하나의 제품(product)의 review(obj)
        reviews = ReviewModel.objects.filter(product=obj)

        if 0 < len(reviews):
            total_rating = 0

            for review in reviews:
                total_rating += review.rating

            avg_rating = total_rating / len(reviews)

            return avg_rating
        else:
            return None

    # 작성된 리뷰는 모두 return하는 것이 아닌 가장 최근 리뷰 1개만 리턴해주세요.
    def get_review(self, obj):
        # 하나의 제품(product)의 review(obj)
        reviews = ReviewModel.objects.filter(product=obj).order_by("-created_at")
        if 0 < len(reviews):
            recent_review = ReviewSerializer(reviews[0]).data
            return recent_review
        else:
            return None

    class Meta:
        model = ProductModel
        fields = ["user", "title", "thumbnail", "description",
        "created_at", "update_at","show_date_start", "show_date_end",
        "price", "is_active", "average_rating", "review"]
