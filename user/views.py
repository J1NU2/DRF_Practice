from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from user.serializers import UserSerializer

from drf_project.permissions import MoreThanThreeDaysUser, IsAdminOrIsAuthenticatedReadOnly

# Create your views here.
# class APIViewPractice(APIView): # CBV 방식
#     # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
#     # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
#     # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

#     def get(self, request):
#         return Response({'message': 'get method!!'})
        
#     def post(self, request):
#         return Response({'message': 'post method!!'})

#     def put(self, request):
#         return Response({'message': 'put method!!'})

#     def delete(self, request):
#         return Response({'message': 'delete method!!'})


class UserView(APIView):
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly] # 사용자 지정 permission

    # 로그인 한 사용자 보여주기
    def get(self, request):
        user = request.user # 로그인한 유저 정보

        if not user.is_authenticated:
            return Response({"fail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # # 역참조를 사용했을 때
        # # 만약 참조할 필드가 one-to-one이라면 _set이 붙지 않는다.
        # hobbys = user.userprofile.hobby.all()

        # # 역참조를 사용하지 않았을 때
        # user_profile = UserProfile.objects.get(user=user)
        # hobbys = user_profile.hobby.all()
        
        return Response(UserSerializer(user, context={"user": user}).data, status=status.HTTP_200_OK)
        # return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    

class UserSignView(APIView):
    permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능

    # 로그인 기능
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"fail": "계정이 존재하지 않거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        return Response({"success": "로그인 완료"}, status=status.HTTP_200_OK)
    
    # 로그아웃
    def delete(self, request):
        logout(request)

        return Response({"success": "로그아웃 완료"}, status=status.HTTP_200_OK)
