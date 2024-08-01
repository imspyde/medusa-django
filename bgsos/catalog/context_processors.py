# In catalog/context_processors.py
from catalog.services.services import get_collections

def cart_id(request):
    return {'cart_id': request.session.get('cart_id')}

def collections_processor(request):
    response = get_collections()
    if response.status_code == 200:
        collections_data = response.json()
        collections = collections_data.get('collections', [])
    else:
        collections = []
    return {'collections': collections}