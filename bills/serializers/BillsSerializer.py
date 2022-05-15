from bills.models import Bills, BillsProducts
from clients.serializers.ClientsSerializer import ListClientsSerializer
from products.models import Products
from products.serializers.ProductsSerializer import ListProductsSerializer
from rest_framework import serializers
    
class ListProductsBillsSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class BillsSerializer(serializers.Serializer):
    client = ListClientsSerializer(required=False)
    client_id = serializers.IntegerField()
    products = ListProductsBillsSerializer(many=True, read_only=False)
    company_name = serializers.CharField(max_length=150)
    nit = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=150)
    
    def validate_products(self, value):
        for item in value:
            product = dict(item)
            product_data = Products.objects.filter(id=product["id"])
            
            if product_data.__len__() == 0:                
                raise serializers.ValidationError("Product not found")
    
        return value
    
    def create(self, validated_data):
        product_list = validated_data.pop("products")
        bill = Bills.objects.create(**validated_data)
        
        for item in product_list:
            product = dict(item)
            
            product_data = Products.objects.get(id=product["id"])
            data = dict()
            data["bill"] = bill
            data["product"] = product_data
            BillsProducts.objects.create(**data)
        
        return bill 

class UpdateBillsSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=150)
    nit = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=150)
    
    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.nit = validated_data.get('nit', instance.nit)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance

class DeleteBillsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    def delete(self, instance):
        instance.delete()
    
class DetailsProductsBillsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = ListProductsSerializer(many=False, read_only=False)
    
class ListBillsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    client = ListClientsSerializer(read_only=True)
    details = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(max_length=150)
    nit = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=150)
    
    class Meta:
        model = Bills
        fields = ['id', 'client', 'details', 'company_name', 'nit', 'code']

    def get_details(self, bill):
        detail = BillsProducts.objects.filter(bill=bill)
        serializer = DetailsProductsBillsSerializer(detail, many=True)
        return serializer.data