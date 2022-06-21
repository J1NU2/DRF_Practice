from rest_framework import serializers

from blog.models import Category
from blog.models import Article
from blog.models import Comment


# 카테고리
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


# 로그인한 사용자의 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ["user", "comment"]


# 로그인한 사용자의 게시글
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, source="comment_set")

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    class Meta:
        model = Article
        fields = ["user", "title", "content", "category", "comments"]
        