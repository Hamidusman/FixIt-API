from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]