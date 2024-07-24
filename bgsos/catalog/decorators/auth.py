from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'auth_token' not in request.session:
            return redirect(reverse('customer_signin'))
        return view_func(request, *args, **kwargs)

    return wrapper
