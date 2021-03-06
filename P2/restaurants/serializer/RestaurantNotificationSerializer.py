from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from restaurants.models import RestaurantNotification


class RestaurantNotificationSerializer(ModelSerializer):
    last_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = RestaurantNotification
        fields = ['restaurant', 'title', 'last_modified']
