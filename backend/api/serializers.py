from rest_framework import serializers
from Iphones.models import Iphone


class IphonesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Iphone
        fields = '__all__'
