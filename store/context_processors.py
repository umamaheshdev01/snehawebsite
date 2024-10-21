from .models import Cart, CartItem

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user_id=request.user)
        count = cart.cart_items.count() 
    return {'cart_item_count': count}