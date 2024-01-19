"""
URL configuration for waste_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from waste.views import indexview,login_view,userRegistration
from waste import admin_urls,user_urls,collector_urls
from waste.admin_views import product_list
from waste.views import shop,view_product,CheckPincodeView,Check

urlpatterns = [
    path('admin/',admin_urls.urls()),
    path('',indexview.as_view()),
    path('Check',Check.as_view()),
    path('login',login_view.as_view()),
    path('UserRegister',userRegistration.as_view()),
    path('user/',user_urls.urls()),
    path('collector/',collector_urls.urls()),
    path('Shop',shop.as_view()),
    path('viewproducts',product_list.as_view()),
    path('Product',view_product.as_view()),
    path('check_pincode/', CheckPincodeView.as_view(), name='check_pincode'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG :
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_URL)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)