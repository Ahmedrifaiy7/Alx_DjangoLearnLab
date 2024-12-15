from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer # Import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'