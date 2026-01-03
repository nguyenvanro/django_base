from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer base for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'avatar', 'bio', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')

    

