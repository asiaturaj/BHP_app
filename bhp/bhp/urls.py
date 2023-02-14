"""bhp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from bhpwoo import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.EmployeeView.as_view(), name='home'),
    path("employee-detail/<int:employee_id>/", views.EmployeeDetailView.as_view(), name='employee_detail'),
    path("protective-clothes/", views.ProtectiveClothesView.as_view(), name='protective_clothes'),
    path("protective-clothes-sets/", views.ProtectiveClothesSetsView.as_view(), name='protective_clothes_sets'),
    path("protective-clothes-set-detail/<int:set_id>/", views.ProtectiveClothesSetDetailView.as_view(), name='protective_clothes_set_detail'),
    path("protective-clothes-sets-released/", views.ProtectiveClothesSetsReleasedView.as_view(), name='protective_clothes_sets_released'),
    path("form/", views.ReleaseFormView.as_view(), name='form'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)