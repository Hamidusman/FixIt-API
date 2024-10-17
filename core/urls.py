from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'booking', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]