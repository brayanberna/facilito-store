from .models import Cart

def get_or_create_cart(request):
  #request.session['cart_id'] = None #Elimina la sessión
  user = request.user if request.user.is_authenticated else None
  cart_id = request.session.get('cart_id')
  cart = Cart.objects.filter(cart_id=cart_id).first() #[] --> None

  if cart is None:
    # Crea un carrito.
    cart = Cart.objects.create(user=user)

  # Si el usuario existe y el carrito no posee un usuario
  if user and cart.user is None:
    # Asigna un usuario al carrito
    cart.user = user
    cart.save()

  # Crear una sessión.
  request.session['cart_id'] = cart.cart_id
  return cart

def destroy_cart(request):
  request.session['cart_id'] = None