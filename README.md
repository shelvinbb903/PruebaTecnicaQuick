## Detalles del proyecto
- Python
- Django
- PostgreSQL
- pgAdmin
- DBeaver

## Instrucciones de Despliegue

Para realizar la verificación de los puntos de la prueba técnica se deben seguir los siguientes pasos:

- Clonar el proyecto, ya sea con el comando git clone https://github.com/shelvinbb903/PruebaTecnicaQuick.git o usando una herramienta grafica GitHub

- Después de clonar el repositorio, acceder a la carpeta descargada con el comando cd en la terminal, ya que en ella se ejecutarán varios comandos.

- Activar enviroment de python con los comandos: 
```
python -m venv env
source env/Scripts/activate
```

- Instalar las dependencias necesarias y usadas para la prueba con el comando: ```pip install -r requirements.txt```

- Crear la base de datos en el administrador de su preferencia. Por ejemplo, puede usar pgAdmin para crear la base de datos y DBeaver para realizar la conexión a la base de datos y ver la estructura de las tablas. Para la prueba, el nombre que se uso fue prueba, pero puede usar otro nombre.

- Cambiar la conexión a la base de datos archivo PruebaTecnica/settings.py del proyecto. En este archivo se modifican el diccionario u objeto DATABASES, el cual tiene los atributos para la conexión establecida por defecto. Se modifican los atributos USER y PASSWORD, los cuales tienen su configuración establecida durante la instalación de PostgreSQL en su equipo y NAME que corresponde al nombre de la base de datos que generó en el paso anterior.

- Ejecutar las migraciones para generar la estructura de las tablas en la base de datos creada. Se realiza con el comando: ```python manage.py migrate```

- En este punto, el proyecto está listo para realizar prueba. Se realiza la ejecución con el comando: ```python manage.py runserver```

## Notas Adicionales

- Después de ejecutar el servicio /users/login/ el token jwt generado (propiedad token del JSON como respuesta) se debe agregar como cabecera o header en las conexiones a los demás servicios api rest, el cual tiene como clave Authorization y su valor es el token. Ejemplo: Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InNoZWx2aW5iYkBnbWFpbC5jb20iLCJleHAiOjE2NTI1OTk0OTB9._U65DUEN4vRSN7H6WvNrOPIgaUASJ9HguDT-qgeq6ZY

- Dentro del proyecto se agregó el archivo como plantilla para la API rest de cargue masivo de clientes con un archivo csv.

- Además se agregó el archivo postman_collections con todas las API rest desarrolladas.

- La API rest de descarga de registros de clientes en un archivo se realiza en el navegador. Se guardó en el archivo postman_collections para recordar la url.
    http://127.0.0.1:8000/clients/download/
