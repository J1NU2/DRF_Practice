from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from blog.models import Article
# from blog.models import Article as ArticleModel로 사용해도 괜찮다.

#CBV 기반으로 로그인 한 사용자의 게시글의 제목을 리턴해주는 기능을 구현해주세요
# Create your views here.
class BlogView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    
    def get(self, request):
        user = request.user

        articles = Article.objects.filter(user=user)
        # titles = []

        # for article in articles:
        #     titles.append(article.title)

        # titles를 아래와 같이 축약할 수 있음(list 축약 문법)

        titles = [article.title for article in articles]
        
        return Response({"article_list": titles})
        