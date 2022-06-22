from rest_framework import serializers

from blog.models import Category as CategoryModel
from blog.models import Comment as CommentModel
from blog.models import Article as ArticleModel


# 카테고리
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["name"]


# 로그인한 사용자의 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = CommentModel
        fields = ["user", "comment"]


# 로그인한 사용자의 게시글
class ArticleSerializer(serializers.ModelSerializer):
    # SerializerMethodField와 read_only=True로 설정되어 있다면
    # validate 를 검증하지 않는다.
    category = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, source="comment_set", read_only=True)

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    class Meta:
        model = ArticleModel
        fields = ["user", "title", "content", "category", "comments"]
        