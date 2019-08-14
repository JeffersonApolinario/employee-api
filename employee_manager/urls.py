"""employee_manager URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from employee_manager_api.views import (
    employee_list_or_create,
    employee_findone_or_update_or_delete,
    department_list_or_create
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('', admin.site.urls),
    path('api/departments', department_list_or_create, name='department_list_or_create'),
    path('api/employees', employee_list_or_create, name='employee_list_or_create'),
    path('api/employees/<int:id>', employee_findone_or_update_or_delete, name='employee_findone_or_update_or_delete'),
    re_path(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair')
]
