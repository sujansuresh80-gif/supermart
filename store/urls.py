from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('products/', views.product_list, name='product_list'),

    path(
    'products/<int:product_id>/',
    views.product_detail,
    name='product_detail'
),

    path(
    'products/<int:product_id>/order/',
    views.add_order,
    name='add_order'
),

    path(
    'orders/',
    views.my_orders,
    name='my_orders'
),
    path(
        'products/add/',
        views.product_create,
        name='product_create'
    ),

    path(
        'products/edit/<int:product_id>/',
        views.product_update,
        name='product_update'
    ),

    path(
        'products/delete/<int:product_id>/',
        views.product_delete,
        name='product_delete'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        LoginView.as_view(
            template_name='store/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]