from products.models import Products
from rest_framework import serializers

class ProductsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=150)
    price = serializers.DecimalField(max_digits=18, decimal_places=2)
    
    def create(self, validated_data):
        product = Products.objects.create(**validated_data)
        return product
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class DeleteProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    def delete(self, instance):
        instance.delete()
    
class ListProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=150)
    price = serializers.DecimalField(max_digits=18, decimal_places=2)
    
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price']