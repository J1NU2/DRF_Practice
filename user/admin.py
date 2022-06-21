from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User, UserProfile, Hobby

# class UserAdmin(admin.ModelAdmin) 직접 설정하려면..
# Inline은 역참조 시 사용이 가능하다.
# Inline 방식은 두가지(TabulaInline(가로) / StackInline(세로))
class UserProfileInline(admin.StackedInline):
    model = UserProfile


# Django Document에서 정의해준 user admin 코드
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('username', 'email', )

    fieldsets = (
        ("info", {'fields': ('username', 'password', 'email', 'fullname', 'join_date',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),)

    filter_horizontal = []

    inlines = (
        UserProfileInline,
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Hobby)
