from django.urls import path
from post import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
]
