## Setup
### Create a venv
```python3 -m venv myenv```

### Activate venv
```source myenv/bin/activate```

### Install Django
```python -m pip install Django==5.0.6```

### Activate python version with pyenv
```pyenv global 3.12.0```
Note this should be done before creating the env

## Create Django project
```django-admin startproject```

## Create services.py and use in the project
```from myapp.services.services import create_cart, add_to_cart, remove_from_cart, get_cart_detail``

## Install socks
```pip install 'requests[socks]'```

## Divide prices by 100
templatetags/custom_filters.py

## Cart Middleware
creates a cart id and stores in the Django session

## Context processor
Gets the cart id
```
def cart_id(request):
    return {'cart_id': request.session.get('cart_id')}
```

## To Do:
### Templates
Catalog: Main store application
- Orders (customer can view orders)
- Checkout: Address
- Payments
- Invoice
#### Changes
Improve template for product pages, store, etc.
- Generic stores the navigation

Root directory
- Login
- Logout
- password reset
- registration