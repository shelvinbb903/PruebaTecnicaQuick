import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from users.models import Users

class JWTAuthenticationMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ Se obtiene el token """
        errors = dict()
        try:
            """ Se verifica si la url ejecutada no corresponde a api rest que no deben ser protegidos con JWT """
            if request.path_info != '/users/login/' and request.path_info != '/users/' and request.path_info != '/clients/download/':
                token = request.META['HTTP_AUTHORIZATION']
                
                """ Se valida si se envia el token """
                if token.__len__() == 0:
                    errors["errors"] = "Invalid token header. No credentials provided."
                    return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=errors)
                
                """ Se decodifica el token """
                payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
                
                """ Se valida si hay datos """
                if payload == None:
                    errors["errors"] = "Invalid user. No credentials provided."
                    return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=errors)
            
                queryset = Users.objects.filter(id=payload["user_id"]) 
            
                """ Se verifica si el usuario del payload del token existe en la base de datos """
                if queryset.__len__() == 0:
                    errors["errors"] = "Invalid credentials. User not found."
                    return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=errors)
            
            return self.get_response(request)
        except:
            errors["errors"] = "Invalid token header. No credentials provided."
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data=errors)