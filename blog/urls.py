from django.urls import path
from blog import views

urlpatterns = [
    # blog/
    path('article/', views.ArticleView.as_view()),
]
