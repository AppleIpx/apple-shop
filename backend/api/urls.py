from django.urls import (
    path,
    include
)
from .views import IphoneListView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register(r'catalog', views.PhonesViewSet)

urlpatterns = [
    path("", views.main),
    path("iphones/", IphoneListView.as_view())
]
