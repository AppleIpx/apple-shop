from django.shortcuts import render
from rest_framework import viewsets


# class PhonesViewSet(viewsets.ModelViewSet):

def main(request):
    return render(request, "api/main.html")
