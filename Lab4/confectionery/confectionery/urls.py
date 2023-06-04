"""
URL configuration for confectionery project.

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
from customers.views import CreateUser, LogoutView, LoginView
from products.views import ProductDelete, ProductDetail, ProductCreate, ProductList, ProductEdit
from orders.views import CreateOrderView, OrderDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/create/', ProductCreate.as_view(), name='product_create'),
    path('products/<int:id>/', ProductDetail.as_view(), name='product_detail'),
    path('products/<int:id>/edit/', ProductEdit.as_view(), name='product_edit'),
    path('products/<int:id>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('register/', CreateUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('order/create/', CreateOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),

]
