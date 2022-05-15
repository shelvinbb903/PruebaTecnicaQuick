"""PruebaTecnica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from bills.views import BillsAPPView
from clients.views import ClientsAPPView, DownloadClientsAPPView, UploadClientsAPPView
from products.views import ProductsAPPView
from users.views import LoginAPPView
from users.views import UsersAPPView

urlpatterns = [
    path('users/login/', LoginAPPView.as_view()),
    path('users/', UsersAPPView.as_view()),
    path('clients/', ClientsAPPView.as_view()),
    path('products/', ProductsAPPView.as_view()),
    path('bills/', BillsAPPView.as_view()),
    path('clients/download/', DownloadClientsAPPView.as_view()),
    path('clients/upload/', UploadClientsAPPView.as_view()),
]
