from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import IphonesListSerializers
from Iphones.models import Iphone


# class PhonesViewSet(viewsets.ModelViewSet):

def main(request):
    return render(request, "api/main.html")


def iphones(request):
    return render(request, "api/iphones.html")


class IphoneListView(generics.ListAPIView):
    serializer_class = IphonesListSerializers
    queryset = Iphone.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
