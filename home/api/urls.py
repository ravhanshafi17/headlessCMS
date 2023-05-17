from django.urls import path, include
from rest_framework import routers
from .views import categories ,PostListAPIView,PostListByIdAPIView,CategoriesByIdAPIView
router = routers.DefaultRouter()

urlpatterns=[
    path('', include(router.urls)),
    path('categories/', categories, name='categories'),
    path('post-list/', PostListAPIView.as_view(), name='PostListAPIView'),
    path('post-id/<int:pk>/', PostListByIdAPIView.as_view(), name='PostListByIdAPIView'),
    path('categories-id/<int:pk>/', CategoriesByIdAPIView.as_view(), name='CategoriesByIdAPIView'),
]