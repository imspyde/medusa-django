import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings  # Import settings from Django

# Get the variables from the settings
backendUrl = settings.BACKEND_URL
publishableApiKey = settings.PUBLISHABLE_API_KEY
regionId = settings.REGION_ID

# Setting up the SOCKS5 proxy
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

# Creating a session and configuring it
session = requests.Session()

# Adding retry strategy
retry = Retry(
    total=10,
    read=10,
    connect=10,
    backoff_factor=1,
    status_forcelist=[502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)

# Mounting the adapter to session
session.mount('http://', adapter)
session.mount('https://', adapter)

# Setting default headers and proxy configuration
session.headers.update({'x-publishable-api-key': publishableApiKey})
session.proxies.update(proxies)

def create_cart():
    return session.post(f'{backendUrl}/store/carts')

def add_to_cart(cart_id, variant_id, qty):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/line-items', json={'variant_id': variant_id, 'quantity': qty})

def remove_from_cart(cart_id, item_id):
    return session.delete(f'{backendUrl}/store/carts/{cart_id}/line-items/{item_id}')

def get_cart_detail(cart_id):
    return session.get(f'{backendUrl}/store/carts/{cart_id}')

def get_products(product_id=None, collection_id=None):
    if product_id:
        return session.get(f'{backendUrl}/store/products/{product_id}')
    elif collection_id:
        return session.get(f'{backendUrl}/store/products', params={'collection_id[]': collection_id})
    else:
        return session.get(f'{backendUrl}/store/products')

def browse_all_products():
    return session.get(f'{backendUrl}/store/products')

def get_collections():
    return session.get(f'{backendUrl}/store/collections')

def get_collection_name(id):
    response = session.get(f'{backendUrl}/store/collections/{id}')
    if response.status_code == 200:
        collection_data = response.json()
        return collection_data['collection']['title']  # Extract the title
    else:
        return None

def update_shipping_details(cart_id, data):
    shipping_address = data
    billing_address = data
    shipping_address['country_code'] = 'au'
    billing_address['country_code'] = 'au'
    return session.post(f'{backendUrl}/store/carts/{cart_id}', json={
        'shipping_address': shipping_address,
        'billing_address': billing_address,
    })

def confirm_order(cart_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/complete')

def update_cart(cart_id, data):
    return session.post(f'{backendUrl}/store/carts/{cart_id}', json=data)

def shipping_method(cart_id, option_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/shipping-methods', json={'option_id': option_id})

def create_payment_session(cart_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/payment-sessions')

def select_payment_session(cart_id, provider_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/payment-session', json={'provider_id': provider_id})

def get_shipping_options():
    return session.get(f'{backendUrl}/store/shipping-options', params={'region_id': regionId})



# New authentication functions

def get_current_customer(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    return session.get(f'{backendUrl}/store/auth', headers=headers)

def customer_login(email, password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'email': email,
        'password': password,
    }
    return session.post(f'{backendUrl}/store/auth', headers=headers, json=data)

def customer_logout(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    return session.delete(f'{backendUrl}/store/auth', headers=headers)

def login_jwt(email, password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'email': email,
        'password': password,
    }
    return session.post(f'{backendUrl}/store/auth/token', headers=headers, json=data)

def check_email_exists(email):
    return session.get(f'{backendUrl}/store/auth/{email}')