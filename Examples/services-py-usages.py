# myapp/views.py

from django.shortcuts import render, redirect
from myapp.services.services import create_cart

def create_cart_view(request):
    response = create_cart()
    if response.status_code == 200:
        cart = response.json()
        return render(request, 'cart_detail.html', {'cart': cart})
    else:
        return render(request, 'error.html', {'message': 'Failed to create cart'})
