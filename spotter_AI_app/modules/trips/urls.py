from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TripViewSet


router = DefaultRouter()

urlpatterns = [
    path('create_trips/', TripViewSet.as_view(), name='create_trips'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls