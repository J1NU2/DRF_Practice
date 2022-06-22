from rest_framework import serializers

from blog.serializers import ArticleSerializer, CommentSerializer

from user.models import Hobby as HobbyModel
from user.models import UserProfile as UserProfileModel
from user.models import User as UserModel


# 취미
class HobbySerializer(serializers.ModelSerializer):
    # 원하는 필드를 추가하고, 다른 Serializer를 사용할 수 있음
    same_hobby_users = serializers.SerializerMethodField()

    def get_same_hobby_users(self, obj): # obj = hobby객체
        user = self.context.get("user")
        # 역참조
        # userprofile = obj.userprofile_set.all()
        userprofiles = obj.userprofile_set.exclude(user=user) # 로그인된 사용자 hobby 제외

        # user_list = []
        # for userprofile in userprofiles:
        #     user_list.append(userprofile.user.username)
        user_list = [userprofile.user.username for userprofile in userprofiles] # list 축약

        return user_list

    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]


# 로그인한 사용자의 상세 정보
class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True)

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]
        # fields = "__all__" # 전체 필드


# 로그인한 사용자의 기본 정보
class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    # many=True : 여러 개의 값을 리스트의 형태로 가져온다.
    # source="이름_set" : article_set에 있는 내용을~
    articles = ArticleSerializer(many=True, source="article_set")
    comments = CommentSerializer(many=True, source="comment_set")

    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "join_date", "userprofile", "articles", "comments"]
