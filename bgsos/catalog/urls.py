# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<str:product_id>/', views.product_detail_view, name='product_detail'),  # Ensure it accepts str
    path('collections/', views.collections_view, name='collections'),
    path('collections/<str:collection_id>/', views.collection_products_view, name='collection_products'),

    # path('cart/', views.create_cart_view, name='create_cart'),
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/<str:cart_id>/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<str:variant_id>/<int:qty>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<str:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<str:item_id>/', views.update_cart_item_view, name='update_cart_item'),
    # path('cart/update/', views.update_cart_items_view, name='update_cart_items'),

    # Other URL patterns

    path('cart/update_shipping/', views.update_shipping_view, name='update_shipping'),
    path('cart/confirm_order/', views.confirm_order_view, name='confirm_order'),
    path('cart/update_cart/', views.update_cart_view, name='update_cart'),
    path('cart/select_shipping/', views.select_shipping_method_view, name='select_shipping'),
    path('cart/create_payment_session/', views.create_payment_session_view, name='create_payment_session'),
    path('cart/select_payment_session/', views.select_payment_session_view, name='select_payment_session'),
    path('cart/add/<str:variant_id>/<int:qty>/', views.add_to_cart_view, name='add_to_cart'),
    path('add-coupon/', views.add_coupon_code, name='add_coupon_code'),
    path('checkout/', views.checkout_view, name='checkout'),  # Add this line
    path('shipping-methods/', views.shipping_methods, name='shipping_methods'),
    path('confirm_order/', views.confirm_order_view, name='confirm_order'),  # Add this line if you have this view

    # User Signup and Login
    path('customer/signup', views.customer_signup, name='customer_signup'),
    path('customer/signin', views.customer_signin, name='customer_signin'),

    path('cart/payment', views.show_usdt_address, name='show_usdt_address'),
    path('cart/show_payment_options', views.show_payment_options, name='show_payment_options'),
    path('payment/show_usdt_address', views.show_usdt_address, name='show_usdt_address'),
    path('payment/show_btc_address', views.show_btc_address, name='show_btc_address'),

    path('customer/profile', views.customer_profile, name='customer_profile'),
    path('customer/logout', views.customer_logout, name='customer_logout'),
    path('customer/change_password', views.change_password, name='change_customer_password'),
    path('customer/orders', views.customer_orders, name='customer_orders')

]
