from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status


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
    permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

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
        