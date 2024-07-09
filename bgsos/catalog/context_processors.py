def cart_id(request):
    return {'cart_id': request.session.get('cart_id')}