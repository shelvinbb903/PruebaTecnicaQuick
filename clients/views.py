import json
from django.http import JsonResponse
from clients.models import Clients
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
import csv

from clients.serializers.ClientsSerializer import ClientsSerializer, DeleteClientsSerializer, DownloadClientsSerializer, ListClientsSerializer, UpdateClientSerializer, UploadClientsSerializer
from users.middleware import JWTAuthenticationMiddleware

class ClientsAPPView(APIView):  
    """ Creacion de clientes """
    def post(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
            
        serializer = ClientsSerializer(data=data)
        """ Se valida si no hay errores la operacion de crear. Si hay errores, se retorna """
        if serializer.is_valid(raise_exception=False):
            client = serializer.create(serializer.data)
            serializer_data = ListClientsSerializer(client, many=False)
            
            response["data"] = serializer_data.data
            return JsonResponse(status=status.HTTP_201_CREATED, data=response)
        else:
            response["errors"] = serializer.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
    
    """ Consulta de clientes registrados
        Se puede listar todos los registros o se puede filtrar la consulta 
        por los campos en la tabla
    """
    def get(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
            
        queryset = Clients.objects.filter(**data)
        serializer = ListClientsSerializer(queryset, many=True)
        response["data"] = serializer.data
        return JsonResponse(status=status.HTTP_200_OK, data=response)
    
    """ Modificar datos de un cliente registrado """
    def patch(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}       
        
        try:
            serializer = UpdateClientSerializer(data=data)
            """ Se valida si no hay errores la operacion de modificar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe el cliente """
                queryset = Clients.objects.get(id=data["id"])    
                client = serializer.update(queryset, data)
                serializer_data = ListClientsSerializer(client)            
                response["data"] = serializer_data.data
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Clients.DoesNotExist:
            response["errors"] = "Client not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
    
    """ Modificar datos de un cliente registrado """
    def delete(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
        
        try:
            serializer = DeleteClientsSerializer(data=data)            
            """ Se valida si no hay errores la operacion de eliminar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe el cliente """
                queryset = Clients.objects.get(id=data["id"])    
                serializer.delete(queryset)       
                response["data"] = {}
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Clients.DoesNotExist:
            response["errors"] = "Client not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        
class DownloadClientsAPPView(APIView):
    """ Descarga de clientes """
    def get(self, request):
        queryset = Clients.objects.all()       
        serializer = DownloadClientsSerializer(queryset, many=True) 
        """ Se realiza la configuracion del archivo a descargar """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="RegistrosClientes.csv"'
        writer = csv.writer(response)
        writer.writerow(['Documento', 'Nombre Completo', 'Cantidad Facturas'])
        
        """ Se itera el listado para agregar cada registro como fila del archivo """
        for item in serializer.data:
            client = dict(item)
            writer.writerow([client["document"], client["full_name"], client["bills_size"]])
        return response
    
class UploadClientsAPPView(APIView):
    """ Cargue masivo de clientes """
    def post(self, request):
        response = dict()
        
        serializer_file = UploadClientsSerializer(data=request.FILES)
        if serializer_file.is_valid(raise_exception=False):
            clients_file = request.FILES["clients_file"]   
        
            """ Se verifica la extension del archivo """
            if not clients_file.name.endswith('.csv'): 
                response["errors"] = "File is not CSV type"
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
            
            """ Se obtienen los registros """
            file_data = clients_file.read().decode("utf-8")
            lines = file_data.split("\r")
            
            """ Se iteran las filas para guardarlas en la base de datos """
            index = 0	
            """ Se iteran los registros, los cuales tienen los valores de las columnas separados por ; """
            for line in lines:                
                data = line.split(";")
                """ Se verifica que el registro iterado no sea la primera fila, que corresponde a los titulos """
                if index > 0:
                    if data[0].strip():
                        client = {}
                        client["document"] = data[0]
                        client["first_name"] = data[1]
                        client["last_name"] = data[2]
                        client["email"] = data[3]                    
                        
                        serializer = ClientsSerializer(data=client)
                        """ Se valida si no hay errores la operacion de crear. Si hay errores, se retorna """
                        if serializer.is_valid(raise_exception=False):
                            serializer.create(serializer.data)               
                        else:
                            response["errors"] = serializer.errors
                            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
                index+=1
                
            response["data"] = {}
            return JsonResponse(status=status.HTTP_201_CREATED, data=response) 
        else:
            response["errors"] = serializer_file.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 