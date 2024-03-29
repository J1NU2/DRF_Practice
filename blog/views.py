from django.db.models.query_utils import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from blog.models import Article, Category
from blog.serializers import ArticleSerializer
# from blog.models import Article as ArticleModel로 사용해도 괜찮다.

from drf_project.permissions import MoreThanThreeDaysUser, IsAdminOrMoreThanOneWeekUser


#CBV 기반으로 로그인 한 사용자의 게시글의 제목을 리턴해주는 기능을 구현해주세요
# Create your views here.
class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [MoreThanThreeDaysUser] # 사용자 지정 permission (3일차)
    # parmission_classes = [IsAdminOrMoreThanOneWeekUser] # 사용자 지정 permission (4일차)

    # 게시글 조회, 로그인한 사용자만 가능
    def get(self, request):
        user = request.user # 로그인한 사용자를 user 변수에 담는다.

        if not user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # articles = Article.objects.filter(user=user)
        # titles = []
        # for article in articles:
        #     titles.append(article.title)

        # titles를 아래와 같이 축약할 수 있음(list 축약 문법)
        # titles = [article.title for article in articles]
        
        # get, filter, exclude 사용 시 Field Lookups 문법
        # __contains : 특정 string이 포함된 object 찾기
        # __startswith / __endswith : 특정 string으로 시작 / 끝나는 object 찾기
        # __gt / __lt / __gte / __lte : 큼(>) / 작(<) / 큼같(>=) / 작같(<=)
        # __in : 특정 list에 포함된 object 찾기

        # 쿼리에서 and(&) 및 or(|) 사용(Q)

        show_date_now = timezone.now()

        terms = Q(user=user) & Q(show_date_start__lte=show_date_now) & Q(show_date_end__gte=show_date_now)
        
        # order_by : queryset 정렬
        # "이름" : 오름차순 / "-이름" : 내림차순 / "?" : 랜덤
        articles = Article.objects.filter(terms).order_by("show_date_start")

        return Response(ArticleSerializer(articles, many=True).data)
    
    # 게시글 작성
    @csrf_exempt
    def post(self, request):
        user = request.user # 로그인한 사용자

        # 제목, 내용, 카테고리 작성
        title = request.data.get("title", "")
        contents = request.data.get("contents", "")
        categories = request.data.get("categories", []) # 카테고리는 여러개라 리스트로
        
        # 조건1. 만약 title이 5자 이하라면 게시글을 작성할 수 없다고 리턴해주세요.
        if (len(title) <= 5):
            return Response({"error": "제목은 5글자 이상 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 조건2. 만약 content가 20자 이하라면 게시글을 작성할 수 없다고 리턴해주세요.
        if (len(contents) <= 20):
            return Response({"error": "내용은 20글자 이상 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 조건3. 만약 카테고리가 지정되지 않았다면 카테고리를 지정해야 한다고 리턴해주세요.
        if not categories:
            return Response({"error": "카테고리가 있어야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # article = Article.objects.create(user=user, title=title, content=content)
        article = Article(
            user=user,
            title=title,
            content=contents,
        )

        # 리스트의 형태로 입력받은 categories는 아직 값이 무엇인지 모른다.
        # 그래서 Category.objects.get(필드명=변수명)을 통해 object의 형태로 받는다.
        
        # category_list 축약
        # category_list = categories
        # for category in category_list:
        #     categorys = Category.objects.get(name=category)
        #     Article.category.add(categorys)
        category_list = [Category.objects.get(name=category) for category in categories]

        article.save()
        # article.category. 를 넣는 방법
        # 1. .add(obj, obj, obj) : 리스트에 들어간 값을 풀어서 하나씩 직접 넣어줌
        # 2. .set(변수명) : 리스트 자체를 넣어줌
        # 3. for문 내 .add(obj) : for문을 돌면서 하나씩 넣어줌
        # 4. .add(*변수명) : 해당 변수 값을 넣어줌
        article.category.set(category_list)

        return Response({"message": "게시글 작성 완료"}, status=status.HTTP_200_OK)
