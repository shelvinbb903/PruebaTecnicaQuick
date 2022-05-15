import email
from django.http import JsonResponse
import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from users.models import User, Users
from users.serializers.UsersSerializer import ListUsersSerializer, LoginUsersSerializer, UsersSerializer
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from django.conf import settings

class LoginAPPView(APIView):
    """ Inicio de sesion de usuarios """
    def post(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
        else:
            data = {}
        try: 
            serializer = LoginUsersSerializer(data=data)
            """ Se valida si no hay errores la operacion de modificar. Si hay errores, se retorna """
            if serializer.is_valid(raise_exception=False):
                """ Se verifica si existe el usuario """
                queryset = Users.objects.get(user=serializer.data["user"], password=serializer.data["password"]) 
                serializer_data = ListUsersSerializer(queryset, many=False)
                
                user = User()
                user.username = queryset.user
                user.password = queryset.password
                user.pk = queryset.id
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                response["data"] = serializer_data.data
                response["token"] = token.decode("utf-8")
                return JsonResponse(status=status.HTTP_200_OK, data=response)
            else:
                response["errors"] = serializer.errors
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
        except Users.DoesNotExist:
            response["errors"] = "User not found"
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
        

class UsersAPPView(APIView):
    """ Creacion de usuarios """
    def post(self, request):
        response = dict()
        if request.body:            
            data = json.loads(request.body)
            data["active"] = True
        else:
            data = {}
            
        serializer = UsersSerializer(data=data)
        """ Se valida si no hay errores la operacion de crear. Si hay errores, se retorna """
        if serializer.is_valid(raise_exception=False):
            """ Se verifica si existe el usuario para no generar un registro repetido """
            queryset = Users.objects.filter(user=data["user"]) 
            if queryset:
                response["errors"] = "Users exists"
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response)
            else:
                user = serializer.create(serializer.data)
                serializer_data = ListUsersSerializer(user, many=False)
                
                response["data"] = serializer_data.data
                return JsonResponse(status=status.HTTP_201_CREATED, data=response)
        else:
            response["errors"] = serializer.errors
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=response) 
