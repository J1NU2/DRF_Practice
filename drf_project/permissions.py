from django.utils import timezone
from datetime import timedelta

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status


class MoreThanThreeDaysUser(BasePermission):
    # message = "가입 후 3일 이상이 지난 사용자만 게시글 작성이 가능합니다."
    message = "가입 후 3분 이상이 지난 사용자만 게시글 작성이 가능합니다."

    def has_permission(self, request, view):
        user = request.user
        # user.is_authenticated : 로그인된 사용자
        # request.user.join_date < (timezone.now() - timedelta(day=3))
        # → 저장된 데이터 값에서 3일을 뺀 값
        # bool : 참이면 True, 거짓이면 False
        # return bool(user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=3)))

        # request.user.join_date < (timezone.now() - timedelta(minutes=3))
        # → 저장된 데이터 값에서 3분을 뺀 값
        return bool(user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(minutes=3)))


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


# 기존 article 생성 기능을 유지할 것.
# article은 admin user 혹은 가입 후 7일이 지난 사용자만 생성 가능하도록 해주세요.
# 조회는 로그인 한 사용자에 대해서만 가능하도록 설정해주세요.
class IsAdminOrMoreThanOneWeekUser(BasePermission):
    # admin은 읽기 쓰기 가능 / 일반 사용자는 읽기만 가능
    SAFE_METHODS = ('GET', ) # 일반 사용자 권한 허용 : GET
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하기 위해서는 로그인이 필요합니다.",
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        # 인증된 사용자가 관리자(admin)일 경우
        if user.is_authenticated and user.is_admin:
            return True
            
        # 사용자가 인증되었고, 가입 후 7일이 지난 사용자일 경우
        if user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=7)):
            return True

        # 사용자가 인증되었고, 권한이 GET일 경우(36줄)
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    # admin은 읽기 쓰기 가능 / 일반 사용자는 읽기만 가능
    SAFE_METHODS = ('GET', ) # 일반 사용자 권한 허용 : GET
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하기 위해서는 로그인이 필요합니다.",
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        # 인증된 사용자가 관리자(admin)일 경우
        if user.is_authenticated and user.is_admin:
            return True
            
        # 사용자가 인증되었고, 권한이 GET일 경우(65줄)
        elif user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False


class IsNotAuthenticatedReadOnlyOrMoreThanThreeDaysUserCreate(BasePermission):
    # 관리자(admin)는 읽기/쓰기 가능
    # 로그인 하지 않는 사용자 : 읽기(GET)
    # 회원가입 후 3일 이상 지난 사용자 : 읽기/쓰기
    SAFE_METHODS = ('GET', ) # 일반 사용자 권한 허용 : GET
    # '접근 권한이 없습니다.'
    message = '관리자 또는 회원가입 후 3일이 지나야 합니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하기 위해서는 로그인이 필요합니다.",
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        # 인증된 사용자가 관리자(admin)일 경우
        if user.is_authenticated and user.is_admin:
            return True

        # 사용자가 인증되었고, 가입 후 3일이 지난 사용자일 경우
        if user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=3)):
            return True

        # 사용자가 인증되었고, 권한이 GET일 경우
        elif user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False
        