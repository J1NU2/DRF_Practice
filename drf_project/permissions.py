from django.utils import timezone
from rest_framework.permissions import BasePermission
from datetime import timedelta

class MoreThanThreeDaysUser(BasePermission):
    message = "가입 후 3일 이상이 지난 사용자만 게시글 작성이 가능합니다."
    test_message = "가입 후 3분 이상이 지난 사용자만 게시글 작성이 가능합니다."

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
        