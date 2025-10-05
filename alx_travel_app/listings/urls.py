from django.urls import path, include
from . import views
from .views import ListingViewSet, BookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('test/', views.test_api, name='test-api'),
    path('', include(router.urls)),
]
