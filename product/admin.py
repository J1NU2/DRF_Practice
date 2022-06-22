from django.contrib import admin
from django.utils.html import mark_safe

from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'image_icon', 'description')
    list_display_links = ('title', 'user', )
    list_filter = ('user', )
    search_fields = ('title', 'user', )

    fieldsets = (
        ("info", {'fields': ('title', 'description', 'created_at',)}),
        ('show_date', {'fields': ('show_date_start', 'show_date_end', )}),
        ('thumbnail', {'fields': ('thumbnail', 'image_tag', )}),
    )

    def get_readonly_fields(self, request, obj=None):
        return ('created_at', 'image_tag', )

    # 상세 페이지 내 이미지
    def image_tag(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="300" height="300"/>')
        return None

    # 이미지 미리보기
    def image_icon(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="100" height="100"/>')
        return None

    # 이미지 태그 글자 수
    image_tag.short_description = "Image"
    image_tag.allow_tags = True


# Register your models here.
admin.site.register(Product, ProductAdmin)
