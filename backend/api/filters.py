from django_filters.rest_framework import FilterSet, filters
from Iphones.models import IphoneRom, Iphone, Color


class IphoneFilter(FilterSet):
    model = filters.CharFilter(
        lookup_expr='icontains',
        label='Модель',
    )
    price = filters.NumberFilter(
        lookup_expr='lte',
        label='Цена (не более)',
    )
    rom = filters.ChoiceFilter(choices=IphoneRom.ROM_CHOICES, label='Объем памяти')
    diagonal = filters.NumberFilter(label='Диагональ экрана')
    color = filters.ModelChoiceFilter(queryset=Color.objects.all(), label='Цвет')

    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')

    class Meta:
        model = Iphone
        fields = ['model', 'price', 'rom', 'diagonal', 'color']

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
