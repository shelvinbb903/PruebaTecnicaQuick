import json
from django.shortcuts import render
from products.models import Products
from products.serializers.ProductsSerializer import DeleteProductsSerializer, ListProductsSerializer, ProductsSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status

class ProductsAPPView(APIView):
    """ Creacion de productos """
    def post(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
            
        serializer = ProductsSerializer(data=data)
        """ Se valida si no hay errores la operacion de crear. Si hay errores, se retorna """
        if serializer.is_valid(raise_exception=False):
            product = serializer.create(serializer.data)
            serializer_data = ListProductsSerializer(product, many=False)
            
            response["data"] = serializer_data.data
            return JsonResponse(status=status.HTTP_201_CREATED, data=response)
        else:
            response["errors"] = serializer.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
    
    """ Consulta de productos registrados
        Se puede listar todos los registros o se puede filtrar la consulta 
        por los campos en la tabla
    """
    def get(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
            
        queryset = Products.objects.filter(**data)
        serializer = ListProductsSerializer(queryset, many=True)
        response["data"] = serializer.data
        return JsonResponse(status=status.HTTP_200_OK, data=response)
    
    """ Modificar datos de un producto registrado """
    def patch(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}       
        
        try:
            serializer = ProductsSerializer(data=data)
            """ Se valida si no hay errores la operacion de modificar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe el producto """
                queryset = Products.objects.get(id=data["id"])    
                product = serializer.update(queryset, data)
                serializer_data = ListProductsSerializer(product)            
                response["data"] = serializer_data.data
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Products.DoesNotExist:
            response["errors"] = "Product not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
    
    """ Modificar datos de un producto registrado """
    def delete(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
        
        try:
            serializer = DeleteProductsSerializer(data=data)            
            """ Se valida si no hay errores la operacion de eliminar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe el producto """
                queryset = Products.objects.get(id=data["id"])    
                serializer.delete(queryset)       
                response["data"] = {}
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Products.DoesNotExist:
            response["errors"] = "Product not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)