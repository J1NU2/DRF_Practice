from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from blog.models import Article
# from blog.models import Article as ArticleModel로 사용해도 괜찮다.

from drf_project.permissions import MoreThanThreeDaysUser


#CBV 기반으로 로그인 한 사용자의 게시글의 제목을 리턴해주는 기능을 구현해주세요
# Create your views here.
class ArticleView(APIView):
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    permission_classes = [MoreThanThreeDaysUser]

    # 게시글 보여주기
    def get(self, request):
        user = request.user # 로그인한 사용자를 user 변수에 담는다.

        articles = Article.objects.filter(user=user)
        # titles = []

        # for article in articles:
        #     titles.append(article.title)

        # titles를 아래와 같이 축약할 수 있음(list 축약 문법)

        titles = [article.title for article in articles]
        
        return Response({"article_list": titles})
        
    # 게시글 작성
    def post(self, request):
        user = request.user # 로그인한 사용자

        # 제목, 내용, 카테고리 작성
        title = request.data.get("title", "")
        content = request.data.get("content", "")
        categories = request.data.get("category", []) # 카테고리는 여러개

        # 조건1. 만약 title이 5자 이하라면 게시글을 작성할 수 없다고 리턴해주세요.
        if (len(title) <= 5):
            return Response({"error": "제목은 5글자 이상 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 조건2. 만약 content가 20자 이하라면 게시글을 작성할 수 없다고 리턴해주세요.
        if (len(content) <= 20):
            return Response({"error": "내용은 20글자 이상 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 조건3. 만약 카테고리가 지정되지 않았다면 카테고리를 지정해야 한다고 리턴해주세요.
        if not len(categories):
            return Response({"error": "카테고리가 있어야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        article = Article(
            user=user,
            title=title,
            content=content,
        )
        article.save()
        article.category.add(*categories)

        return Response({"message": "게시글 작성 완료"}, status=status.HTTP_200_OK)
