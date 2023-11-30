from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .pagination import CustomPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from Iphones.models import (
    Iphone,
    ShoppingCart,
    Favorite,
)
from users.models import User
from .filters import IphoneFilter
from .serializers import (
    IphonesListSerializers,
    UserSerializer,
    ShoppingCartSerializers,
    FavoriteSerializers,
    CreateUserSerializer,
    UserReadSerializer,
    PasswordSerializer,
)
from .serializers import ShowIphoneSerializers


# class PhonesViewSet(viewsets.ModelViewSet):

def main(request):
    return render(request, "api/main.html")


# -------------------------------------
#                   User
# -------------------------------------

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None

    # def get_serializer_class(self):
    #     if self.action in ('list', 'retrieve'):
    #         return UserReadSerializer
    #     return CreateUserSerializer

    @action(detail=False, methods=['get'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(
        ["post"],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_password = request.data.get("new_password")
            current_password = request.data.get("current_password")
            if user.check_password(current_password):
                if new_password == current_password:
                    raise serializers.ValidationError(
                        {'new_password': 'Новый пароль должен отличаться от текущего.'}
                    )
                user.set_password(new_password)
                user.save()
                return Response({"status": "password set"})
            else:
                raise serializers.ValidationError(
                    {'current_password': 'Неправильный пароль.'}
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# --------------------------------------
#                   End_User
# --------------------------------------


class IphoneView(viewsets.ModelViewSet):
    serializer_class = ShowIphoneSerializers
    queryset = Iphone.objects.all()
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IphoneFilter
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    # метод, который выводит iphones по первым буквам
    def get_queryset(self):
        name = str(self.request.query_params.get("name"))
        queryset = self.queryset
        if not name:
            return queryset
        start_queryset = queryset.filter(name__istartswith=name)
        return start_queryset

    # def get_serializer_class(self):
    #     method = self.request.method
    #     if method == "GET":
    #         return ShowIphoneSerializers


class FavoriteView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=["post", ], detail=True, )
    def post(self, request, iphone_id):
        user = request.user
        data = {"user": user, "iphone": iphone_id}
        if Favorite.objects.filter(
            user=user,
            iphone_id=iphone_id,
        ).exists():
            return Response(
                {"Ошибка": "Вы уже добавили в избранное"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = FavoriteSerializers(
                data=data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["DELETE", ], detail=True, )
    def delete(self, request, iphone_id):
        user = request.user
        iphone = get_object_or_404(Iphone, id=iphone_id)
        if not Favorite.objects.filter(
                user=user,
                iphone=iphone
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get(user=user, iphone=iphone).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    @action(methods=["post", ], detail=True, )
    def post(self, request, iphone_id):
        user = request.user
        data = {"user": user, "iphone": iphone_id}
        if ShoppingCart.objects.filter(
            user=user,
            iphone_id=iphone_id,
        ).exists():
            return Response(
                {"Ошибка": "Вы уже добавили в корзину"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = ShoppingCartSerializers(
                data=data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["delete", ], detail=True, )
    def post(self, request, iphone_id):
        user = request.user
        iphone = get_object_or_404(Iphone, id=iphone_id)
        if not ShoppingCart.objects.filter(
                user=user,
                iphone=iphone
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.get(user=user, iphone=iphone).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
