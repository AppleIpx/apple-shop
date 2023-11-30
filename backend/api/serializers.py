from rest_framework import serializers
from Iphones.models import (
    Iphone,
    Favorite,
    ShoppingCart,
)
# from users.models import User
# from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions

User = get_user_model()


# -------------------------------------------
# -------------USER--------------------------
# -------------------------------------------

class UserReadSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        )


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'password'
        )


class TokenSerializer(serializers.ModelSerializer):
    # source="key" означает, что в таблице token будет заполнено key
    token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("token",)


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    # в запросе обязательно должен быть пароль
    current_password = serializers.CharField(required=True)

    def validate(self, obj):
        try:
            validate_password(obj['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        return super().validate(obj)

    class Meta:
        model = User
        fields = "__all__"

# -------------------------------------------
# --------------END_USER---------------------
# -------------------------------------------


class IphonesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Iphone
        fields = '__all__'


class ShowIphoneSerializers(serializers.ModelSerializer):
    """Без характеристик"""
    # image = Base64ImageField()
    user = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField("get_is_favorite")
    is_in_shopping_cart = serializers.SerializerMethodField("get_is_in_shopping_cart")

    class Meta:
        model = Iphone
        fields = (
            "id",
            "is_favorited",
            "is_in_shopping_cart",
            "model",
            "image",
            "text",
            "rom",
            "color",
            "mobile_connection",
            "price",
            'user',
        )

    def get_is_favorite(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Favorite.objects.filter(
            iphone=obj,
            user=user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return ShoppingCart.objects.filter(
            iphone=obj,
            user=user
        ).exists()


class SpecIphoneSerializers(ShowIphoneSerializers):
    class Meta:
        model = Iphone
        fields = (
            "id",
            "is_favorited",
            "is_in_shopping_cart",
            "model",
            "image",
            "text",
            "rom",
            "color",
            "mobile_connection",
            "price",
            "processor"
            "screen"
        )


class FavoriteSerializers(serializers.ModelSerializer):
    iphone = serializers.PrimaryKeyRelatedField(
        queryset=Iphone.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Favorite
        fields = (
            "iphone",
            "user"
        )


class ShoppingCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            "iphone",
            "user"
        )
