from rest_framework import serializers

from blog.serializers import ArticleSerializer, CommentSerializer

from user.models import User
from user.models import UserProfile


# 로그인한 사용자의 기본 정보
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["introduction", "birthday", "age"]
        # fields = "__all__" # 전체 필드


# 로그인한 사용자의 상세 정보
class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    # many=True : 여러 개의 값을 리스트의 형태로 가져온다.
    # source="이름_set" : article_set에 있는 내용을~
    articles = ArticleSerializer(many=True, source="article_set")
    comments = CommentSerializer(many=True, source="comment_set")

    class Meta:
        model = User
        fields = ["username", "email", "fullname", "join_date", "userprofile", "articles", "comments"]
