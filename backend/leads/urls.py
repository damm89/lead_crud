from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.LeadViewSet, basename='lead')

app_name = 'leads'

urlpatterns = [
    path('',include(router.urls)),
]