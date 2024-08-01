import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

from urllib3.util.retry import Retry
from django.conf import settings  # Import settings from Django

# Get the variables from the settings
backendUrl = settings.BACKEND_URL
publishableApiKey = settings.PUBLISHABLE_API_KEY
regionId = settings.REGION_ID
btc_url = settings.BTC_URL
btc_store_id = settings.BTC_STORE_ID
btc_store_api = settings.BTC_STORE_API

# Setting up the SOCKS5 proxy
# Comment out to disable proxy

# proxies = {
#     'http': 'socks5h://127.0.0.1:9050',
#     'https': 'socks5h://127.0.0.1:9050',
# }

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



# Comment out to disable proxy
# session.proxies.update(proxies)

# Comment out to disable proxy
session.proxies.update(proxies)



def create_cart():
    response = session.post(f'{backendUrl}/store/carts')
    if response.status_code == 200:
        cart_data = response.json()
        cart = cart_data.get('cart')
        if cart:
            return cart
        else:
            raise Exception("Cart creation failed, no cart data returned")
    else:
        raise Exception(f"Failed to create cart: {response.status_code}, {response.text}")


def add_to_cart(cart_id, variant_id, qty):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/line-items',
                        json={'variant_id': variant_id, 'quantity': qty})


def update_line_item(cart_id, line_id, quantity):
    url = f'{backendUrl}/store/carts/{cart_id}/line-items/{line_id}'
    response = session.post(url, json={"quantity": quantity})
    response.raise_for_status()
    return response.json()


def remove_from_cart(cart_id, item_id):
    return session.delete(f'{backendUrl}/store/carts/{cart_id}/line-items/{item_id}')


def get_cart_detail(cart_id):
    return session.get(f'{backendUrl}/store/carts/{cart_id}')


def update_line_item(cart_id, line_id, quantity):
    url = f'{backendUrl}/store/carts/{cart_id}/line-items/{line_id}'
    response = session.post(url, json={"quantity": quantity})
    response.raise_for_status()
    return response.json()


def update_cart(cart_id, data):
    return session.post(f'{backendUrl}/store/carts/{cart_id}', json=data)


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
    headers = {
        'Content-Type': 'application/json'
    }
    return session.post(f'{backendUrl}/store/carts/{cart_id}', headers=headers, json={
        "shipping_address": {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "address_1": data.get('address_1'),
            "address_2": data.get('address_2'),
            "city": data.get('city'),
            "province": data.get('state'),
            "postal_code": data.get('postal_code'),
            "phone": data.get('phone'),
            "country_code": "au"
        },
        "billing_address": {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "address_1": data.get('address_1'),
            "address_2": data.get('address_2'),
            "city": data.get('city'),
            "province": data.get('state'),
            "postal_code": data.get('postal_code'),
            "phone": data.get('phone'),
            "country_code": "au"
        },
        "email": data.get('email')
    })


def confirm_order(cart_id):
    print('CartId', cart_id)
    return session.post(f'{backendUrl}/store/carts/{cart_id}/complete')


def update_line_item(cart_id, line_id, quantity):
    url = f'{backendUrl}/store/carts/{cart_id}/line-items/{line_id}'
    response = session.post(url, json={"quantity": quantity})
    response.raise_for_status()
    return response.json()


def update_cart(cart_id, data):
    return session.post(f'{backendUrl}/store/carts/{cart_id}', json=data)


def shipping_method(cart_id, option_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/shipping-methods', json={'option_id': option_id})


def create_payment_session(cart_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/payment-sessions')


def select_payment_session(cart_id, provider_id):
    return session.post(f'{backendUrl}/store/carts/{cart_id}/payment-session', json={'provider_id': provider_id})


def get_shipping_options(cart_id):
    return session.get(f'{backendUrl}/store/shipping-options/{cart_id}')


# New authentication functions

def get_current_customer(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    return session.get(f'{backendUrl}/store/auth', headers=headers)


def create_payment(params):
    print(btc_url)
    url = f"{btc_url}/api/v1/stores/{btc_store_id}/invoices"
    headers = {
        "Authorization": f"token {btc_store_api}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": params['amount'],
        "currency": params['currency'],
    }
    response = requests.post(url, headers=headers, json=data)
    return response


def get_invoice_details(params, invoice_id):
    url = f"{btc_url}/api/v1/stores/{params['store_id']}/invoices/{invoice_id}/payment-methods"
    headers = {
        "Authorization": f"token {btc_store_api}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response


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


def create_customer(data):
    headers = {
        'Content-Type': 'application/json'
    }
    data: data
    return session.post(f'{backendUrl}/store/customers', headers=headers, json=data)


def get_customer_profile(auth_token):
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    return session.get(f'{backendUrl}/store/customers/me', headers=headers)


def change_customer_password(auth_token, new_password):
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    data = {
        'password': new_password
    }
    return session.post(f'{backendUrl}/store/customers/me', headers=headers, json=data)


def my_orders(auth_token, offset=0, limit=10):
    print(auth_token)
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    print(f'{backendUrl}/store/customers/me/orders?offset={offset}&limit={limit}')
    return session.get(f'{backendUrl}/store/customers/me/orders?offset={offset}&limit={limit}', headers=headers)
