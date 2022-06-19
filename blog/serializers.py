from rest_framework import serializers

from blog.models import Article
from blog.models import Comment


# 로그인한 사용자의 게시글
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "category", "content"]


# 로그인한 사용자의 댓글
class CommentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = Comment
        fields = ["comment", "article"]
