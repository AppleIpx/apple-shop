from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'iphones', views.IphoneView, basename="iphones")
router.register(r'users', views.UserView, basename="users")

urlpatterns = [
    # path("", views.main),
    path("iphones/<int:recipe_id>/favorite/", views.FavoriteView.as_view()),
    path("iphones/<int:recipe_id>/shopping_cart/", views.ShoppingCartView.as_view()),
    path(r'auth/', include('djoser.urls.authtoken')),
    path("", include(router.urls)),
]
