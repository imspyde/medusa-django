# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<str:product_id>/', views.product_detail_view, name='product_detail'),  # Ensure it accepts str
    
    path('cart/', views.create_cart_view, name='create_cart'),
    path('cart/<int:cart_id>/', views.cart_detail_view, name='cart_detail'),
    path('cart/<int:cart_id>/add/<int:variant_id>/<int:qty>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/<int:cart_id>/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('collections/', views.collections_view, name='collections'),
    path('collections/<str:collection_id>/', views.collection_products_view, name='collection_products'),
    
    path('cart/<int:cart_id>/update_shipping/', views.update_shipping_view, name='update_shipping'),
    path('cart/<int:cart_id>/confirm_order/', views.confirm_order_view, name='confirm_order'),
    path('cart/<int:cart_id>/update_cart/', views.update_cart_view, name='update_cart'),
    path('cart/<int:cart_id>/select_shipping/', views.select_shipping_method_view, name='select_shipping'),
    path('cart/<int:cart_id>/create_payment_session/', views.create_payment_session_view, name='create_payment_session'),
    path('cart/<int:cart_id>/select_payment_session/', views.select_payment_session_view, name='select_payment_session'),
    path('cart/add/<str:variant_id>/<int:qty>/', views.add_to_cart_view, name='add_to_cart'),
    

]
