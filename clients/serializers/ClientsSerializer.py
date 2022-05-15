from bills.models import Bills
from rest_framework import serializers

from clients.models import Clients

class ClientsSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()

    """ Validar existencia del documento """
    def validate_document(self, value):
        client_data = Clients.objects.filter(document=value)
            
        if client_data.__len__() > 0:                
            raise serializers.ValidationError("Document exists")
        
        return value
    
    """ Validar existencia del documento """
    def validate_email(self, value):
        client_data = Clients.objects.filter(email=value)
            
        if client_data.__len__() > 0:                
            raise serializers.ValidationError("Email exists")
        
        return value
    
    def create(self, validated_data):
        client = Clients.objects.create(**validated_data)
        return client   
    
class UpdateClientSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    
    def update(self, instance, validated_data):
        instance.document = validated_data.get('document', instance.document)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class DeleteClientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    def delete(self, instance):
        instance.delete()
    
class ListClientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    document = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    
    class Meta:
        model = Clients
        fields = ['id', 'document', 'first_name', 'last_name', 'email']
        
    
class DownloadClientsSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=20)
    full_name = serializers.SerializerMethodField(read_only=True)
    bills_size = serializers.SerializerMethodField(read_only=True)
    
    def get_full_name(self, client):
        return client.first_name + " " + client.last_name
    
    def get_bills_size(self, client):
        bills = Bills.objects.filter(client=client)
        return bills.__len__()        
    
class UploadClientsSerializer(serializers.Serializer):
    clients_file = serializers.FileField()