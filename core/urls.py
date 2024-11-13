from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'booking', views.BookingViewSet, basename='booking')
router.register(r'rating', views.RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]