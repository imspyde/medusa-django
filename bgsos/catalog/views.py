from django.shortcuts import render

# Create your views here.
# myapp/views.py
# myapp/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from catalog.services.services import (
    create_cart,
    add_to_cart,
    remove_from_cart,
    get_cart_detail,
    get_products,
    browse_all_products,
    get_collections,
    get_collection_name,
    update_shipping_details,
    confirm_order,
    update_cart,
    shipping_method,
    create_payment_session,
    select_payment_session,
    get_shipping_options,
)

##
def index_view(request):
    # Mock data for demonstration
    num_products = 50  # Replace with actual logic to get product count
    num_collections = 10  # Replace with actual logic to get collection count
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Get the product list
    products = get_product_list()

    # Get collections
    response = get_collections()
    if response.status_code == 200:
        collections_data = response.json()
        collections = collections_data.get('collections', [])
    else:
        collections = []

    context = {
        'num_products': num_products,
        'num_collections': num_collections,
        'num_visits': num_visits,
        'featured_products': products[:3],  # Show the first 3 products as featured
        'collections': collections,  # Add collections to context
    }
    
    return render(request, 'index.html', context)

### Product list for index
def get_product_list():
    response = browse_all_products()
    if response.status_code == 200:
        products_data = response.json()
        return products_data.get('products', [])
    else:
        return []
##
def product_list_view(request):
    response = browse_all_products()
    print(response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        products_data = response.json()
        print(products_data)  # Print the parsed JSON response for debugging
        products = products_data.get('products', [])
        return render(request, 'product_list.html', {'products': products})
    else:
        print(f"Failed to load products: {response.status_code}")  # Print the status code if the request failed
        return render(request, 'error.html', {'message': 'Failed to load products'})


def product_detail_view(request, product_id):
    response = get_products(product_id=product_id)
    if response.status_code == 200:
        product = response.json().get('product')
        print(product)
        return render(request, 'product_detail.html', {'product': product})
    else:
        return render(request, 'error.html', {'message': 'Failed to load product'})


## Add to cart view
def add_to_cart_view(request, variant_id, qty):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return redirect('index')

    response = add_to_cart(cart_id, variant_id, qty)
    if response.status_code == 200:
        return redirect('cart_detail', cart_id=cart_id)
    else:
        return render(request, 'error.html', {'message': 'Failed to add item to cart'})
##


def create_cart_view(request):
    response = create_cart()
    if response.status_code == 200:
        cart = response.json()
        return render(request, 'cart_detail.html', {'cart': cart})
    else:
        return render(request, 'error.html', {'message': 'Failed to create cart'})

def add_to_cart_view(request, cart_id, variant_id, qty):
    response = add_to_cart(cart_id, variant_id, qty)
    if response.status_code == 200:
        return redirect('cart_detail', cart_id=cart_id)
    else:
        return render(request, 'error.html', {'message': 'Failed to add to cart'})

def remove_from_cart_view(request, cart_id, item_id):
    response = remove_from_cart(cart_id, item_id)
    if response.status_code == 200:
        return redirect('cart_detail', cart_id=cart_id)
    else:
        return render(request, 'error.html', {'message': 'Failed to remove from cart'})

def cart_detail_view(request, cart_id):
    response = get_cart_detail(cart_id)
    if response.status_code == 200:
        cart = response.json()
        return render(request, 'cart_detail.html', {'cart': cart})
    else:
        return render(request, 'error.html', {'message': 'Failed to load cart'})

## WORKS
def collections_view(request):
    response = get_collections()
    print(response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        collections_data = response.json()
        print(collections_data)  # Print the parsed JSON response for debugging
        collections = collections_data.get('collections', [])
        return render(request, 'collections.html', {'collections': collections})
    else:
        print(f"Failed to load collections: {response.status_code}")  # Print the status code if the request failed
        return render(request, 'error.html', {'message': 'Failed to load collections'})
## END WORKS

def collection_products_view(request, collection_id):
    response = get_products(collection_id=collection_id)
    collection = get_collection_name(collection_id)
    print(collection)
    #products = Product.objects.filter(collection=collection)
    print(response.text)  # Print the raw response text for debugging
    if response.status_code == 200:
        products_data = response.json()  # Parse the JSON response
        print(products_data)  # Print the parsed JSON response for debugging
        products = products_data.get('products', [])  # Extract the products list
        return render(request, 'collection_products.html', {'collection': collection,'products': products})  # Pass to template
    else:
        print(f"Failed to load products: {response.status_code}")  # Print the status code if the request failed
        return render(request, 'error.html', {'message': 'Failed to load products'})


def update_shipping_view(request, cart_id):
    if request.method == 'POST':
        data = request.POST.dict()
        response = update_shipping_details(cart_id, data)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'error.html', {'message': 'Failed to update shipping details'})
    else:
        return render(request, 'update_shipping.html', {'cart_id': cart_id})

def confirm_order_view(request, cart_id):
    response = confirm_order(cart_id)
    if response.status_code == 200:
        return render(request, 'order_confirmation.html', {'order': response.json()})
    else:
        return render(request, 'error.html', {'message': 'Failed to confirm order'})

def update_cart_view(request, cart_id):
    if request.method == 'POST':
        data = request.POST.dict()
        response = update_cart(cart_id, data)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'error.html', {'message': 'Failed to update cart'})
    else:
        return render(request, 'update_cart.html', {'cart_id': cart_id})

def select_shipping_method_view(request, cart_id):
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        response = shipping_method(cart_id, option_id)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'error.html', {'message': 'Failed to select shipping method'})
    else:
        shipping_options = get_shipping_options().json()
        return render(request, 'select_shipping_method.html', {'cart_id': cart_id, 'shipping_options': shipping_options})

def create_payment_session_view(request, cart_id):
    response = create_payment_session(cart_id)
    if response.status_code == 200:
        return redirect('cart_detail', cart_id=cart_id)
    else:
        return render(request, 'error.html', {'message': 'Failed to create payment session'})

def select_payment_session_view(request, cart_id):
    if request.method == 'POST':
        provider_id = request.POST.get('provider_id')
        response = select_payment_session(cart_id, provider_id)
        if response.status_code == 200:
            return redirect('cart_detail', cart_id=cart_id)
        else:
            return render(request, 'error.html', {'message': 'Failed to select payment session'})
    else:
        # Assuming you have a way to get available payment providers
        payment_providers = [{"id": "provider_1", "name": "Provider 1"}, {"id": "provider_2", "name": "Provider 2"}]
        return render(request, 'select_payment_session.html', {'cart_id': cart_id, 'payment_providers': payment_providers})