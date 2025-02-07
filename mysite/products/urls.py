from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/add_to_cart/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('cart/checkout_cart', views.checkout_cart, name='checkout_cart'),
    path('<int:product_id>/edit_cart/<int:updated_quantity>/', views.edit_cart, name='edit_cart'),
    path('order', views.order, name='order'),
    # Two path 1 method for optional param
    path('marketplace', views.marketplace, name='marketplace'),
    # path('marketplace/<str:category>/', views.marketplace, name='marketplace'),
    path('create_product_like/<int:product_id>/', views.create_product_like, name='create_product_like')
]
