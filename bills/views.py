import json
from django.shortcuts import render
from django.http import JsonResponse
from bills.models import Bills
from bills.serializers.BillsSerializer import BillsSerializer, DeleteBillsSerializer, ListBillsSerializer, UpdateBillsSerializer
from clients.models import Clients
from clients.serializers.ClientsSerializer import ListClientsSerializer
from rest_framework.views import APIView
from rest_framework import status

class BillsAPPView(APIView):
    """ Creacion de facturas """
    def post(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
            
        serializer = BillsSerializer(data=data)
        """ Se valida si no hay errores la operacion de crear. Si hay errores, se retorna """
        if serializer.is_valid(raise_exception=False):
            try:
                """ Se verifica si existe el cliente """
                client_data = Clients.objects.get(id=data["client_id"])
                serializer.data["client"] = client_data
                
                bill = serializer.create(serializer.data)
                serializer_data = ListBillsSerializer(bill, many=False)
                response["data"] = serializer_data.data
                return JsonResponse(status=status.HTTP_201_CREATED, data=response)
            except Clients.DoesNotExist:
                response["errors"] = "Client not found"
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
        else:
            response["errors"] = serializer.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
    
    """ Consulta de facturas registradas
        Se puede listar todos los registros o se puede filtrar la consulta 
        por los campos en la tabla
    """
    def get(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
            
        queryset = Bills.objects.filter(**data)
        serializer = ListBillsSerializer(queryset, many=True)
        response["data"] = serializer.data
        return JsonResponse(status=status.HTTP_200_OK, data=response)
    
    """ Modificar datos de una factura registrada """
    def patch(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}       
        
        try:
            serializer = UpdateBillsSerializer(data=data)
            """ Se valida si no hay errores la operacion de modificar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe la factura """
                queryset = Bills.objects.get(id=data["id"])    
                bill = serializer.update(queryset, data)
                serializer_data = ListBillsSerializer(bill)            
                response["data"] = serializer_data.data
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Bills.DoesNotExist:
            response["errors"] = "Bill not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
    
    """ Modificar datos de una factura registrada """
    def delete(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
        
        try:
            serializer = DeleteBillsSerializer(data=data)            
            """ Se valida si no hay errores la operacion de eliminar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe la factura """
                queryset = Bills.objects.get(id=data["id"])    
                serializer.delete(queryset)       
                response["data"] = {}
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Bills.DoesNotExist:
            response["errors"] = "Bill not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 