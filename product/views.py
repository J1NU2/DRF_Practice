from django.db.models.query_utils import Q
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from product.models import Product as ProductModel
from product.serializers import ProductSerializer

# Create your views here.
class ProductView(APIView):
    # 제품 조회
    def get(self, request):
        user = request.user # 로그인된 사용자

        if not user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        show_date_now = timezone.now()

        terms = Q(show_date_start__lte=show_date_now) & Q(show_date_end__gte=show_date_now)

        products = ProductModel.objects.filter(terms).order_by("show_date_start")

        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

    # 제품 등록
    def post(self, request):
        request.data["user"] = request.user.id.username
        product_serializer = ProductSerializer(data=request.data)

        # validate 검증, 검증 시 저장하고 Response 반환
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
            # return Response({"success": "제품 등록 완료"}, status=status.HTTP_200_OK)

        # 검증 실패 시 .errors를 통해 어디가 실패했는지 알려준다.
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 제품 수정
    def put(self, request, product_id):
        # product_id = 해당 product의 pk값
        product = ProductModel.objects.get(id=product_id)
        # 전체 수정이 아닌 부분적으로 수정하고 싶다면 partial=True 사용
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        
        # validate 검증, 검증 시 저장하고 Response 반환
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
            # return Response({"success": "제품 수정 완료"}, status=status.HTTP_200_OK)

        # 검증 실패 시 .errors를 통해 어디가 실패했는지 알려준다.
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
