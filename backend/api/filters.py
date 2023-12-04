from django_filters.rest_framework import FilterSet, filters
from Iphones.models import (
    IphoneRom,
    Iphone,
    IphoneColor,
    IphoneCountCamera,
    IphoneMobileConnection,
    IphoneTypeOfScreen,
    IphoneDiagonal,
    IphoneProcessor,
    IphoneModel,
)


class IphoneFilter(FilterSet):
    model = filters.ModelChoiceFilter(
        queryset=IphoneModel.objects.all(),
        label="Модель iPhone"
    )
    price = filters.NumberFilter(
        lookup_expr='lte',
        label='Цена (не более)',
    )
    rom = filters.ModelChoiceFilter(
        queryset=IphoneRom.objects.all(),
        label='Объем памяти',
    )
    color = filters.ModelChoiceFilter(
        queryset=IphoneColor.objects.all(),
        label='Цвет',
    )
    # diagonal = filters.NumberFilter(label='Диагональ экрана')
    diagonal = filters.ModelChoiceFilter(
        queryset=IphoneDiagonal.objects.all(),
        label="Диагональ",
    )
    mobile_connection = filters.ModelChoiceFilter(
        queryset=IphoneMobileConnection.objects.all(),
        label='Связь',
    )
    camera = filters.ModelChoiceFilter(
        queryset=IphoneCountCamera.objects.all(),
        label="Кол-во камер",
    )
    screen = filters.ModelChoiceFilter(
        queryset=IphoneTypeOfScreen.objects.all(),
        label="Тип экрана",
    )
    processor = filters.ModelChoiceFilter(
        queryset=IphoneProcessor.objects.all(),
        label="Процессор iPhone",
    )

    class Meta:
        model = Iphone
        fields = ['model', 'price',
                  'rom', 'diagonal',
                  'color', 'mobile_connection',
                  'camera', 'screen',
                  'processor',
                  ]

        # метод, который выводит iphones по первым буквам
    def get_models(self):
        name = str(self.request.query_params.get("name"))
        queryset = self.queryset
        if not name:
            return queryset
        start_queryset = queryset.filter(name__istartswith=name)
        return start_queryset

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite_iphone__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_iphone__user=user)
        return queryset
