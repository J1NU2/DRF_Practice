from rest_framework import serializers

from product.models import Product as ProductModel


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
        "created_at", "show_date_start", "show_date_end"]

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
    