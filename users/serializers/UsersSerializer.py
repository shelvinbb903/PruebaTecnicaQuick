from pkg_resources import require
from rest_framework import serializers
from users.models import Users
import base64

class LoginUsersSerializer(serializers.Serializer):
    user = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    
    class Meta:
        model = Users
        
    def validate_password(self, password):
        password = base64.b64encode(bytes(password, 'utf-8'))
        return password

class UsersSerializer(serializers.Serializer):
    user = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    active = serializers.BooleanField(required=False)
    
    class Meta:
        model = Users
        optional_fields = ['active', ]
        
    def validate_password(self, password):
        password = base64.b64encode(bytes(password, 'utf-8'))
        return password
    
    def create(self, validated_data):        
        user = Users.objects.create(**validated_data)
        return user
    
    
class ListUsersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=200)
    active = serializers.BooleanField()