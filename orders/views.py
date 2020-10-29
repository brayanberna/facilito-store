from django.shortcuts import render
from carts.utils import get_or_create_cart
from .models import Order
from .utils import get_or_create_order
from django.contrib.auth.decorators import login_required

from .utils import breadcrumb
from django.shortcuts import get_object_or_404
from shipping_addresses.models import ShippingAddress
from django.shortcuts import redirect
from django.contrib import messages

from .utils import destroy_order
from carts.utils import destroy_cart

from .mails import Mail

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from django.db.models.query import EmptyQuerySet
from.decorators import validate_cart_and_order

import threading

# Create your views here.
class OrderListView(LoginRequiredMixin, ListView):
  login_url = 'login'
  template_name = 'orders/orders.html'

  def get_queryset(self):
    return self.request.user.orders_completed() #Este metodo se crea en users/models.py

@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):

  return render(request, 'order.html', {
    'cart':cart,
    'order':order,
    'breadcrumb': breadcrumb()
  })

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses()

    return render(request, 'orders/address.html', {
      'cart':cart,
      'order':order,
      'breadcrumb': breadcrumb(address=True),
      'shipping_address': shipping_address,
      'can_choose_address': can_choose_address
    })

@login_required(login_url='login')
def select_address(request):
  shipping_addresses = request.user.addresses
  return render(request, 'orders/select_address.html',{
    'breadcrumb': breadcrumb(address=True),
    'shipping_addresses': shipping_addresses,
  })

@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart, order, pk):
  #cart = get_or_create_cart(request) # Obtiene el carrito de compras, Para poder obtener la orden de compra.
  #order = get_or_create_order(cart, request)  # Obtenemos la orden de compra.

  shipping_address = get_object_or_404(ShippingAddress, pk=pk) # Obtiene la dirección que el usuario seleccionó.

  if request.user.id != shipping_address.user_id: # Validando que sea el usuario el que cre´´o la validación
    return redirect('carts:cart')

  # El metodo orders/models.py/'update_shipping_address' establece una dirección de envío.
  order.update_shipping_address(shipping_address) # Actualiza la order con la nueva dirección

  return redirect('orders:address') # orden/direccion

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):

  # La orden de compra tiene que poseer una dirección
  shipping_address = order.shipping_address # Obtiene la dirección de la orden.
  if shipping_address is None:  # Si no posee una dirección de envío.
    return redirect('orders:address') # retorna a 'orden/direccion'
  
  return render(request, 'orders/confirm.html', {
    'cart': cart,
    'order': order,
    'shipping_address': shipping_address,
    'breadcrumb': breadcrumb(address=True, payment=True, confirmation=True)
  })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):
  if request.user.id != order.user_id: # Si no es el mismo usuario quien creo la orden y quien la quiere cancelar.
    return redirect('carts:cart') # Retorna 'http://127.0.0.1:8000/carrito/'
  
  # Este metodo se crea en 'orders/models'
  order.cancel()  # Modifica su estatus a CANCELLED

  # Destruir sessiones del carrito de compra y orden
  # carts/utils.py
  destroy_cart(request) # Elimina la sessión cart
  # orders/utils.py   funciones
  destroy_order(request)  # Eliminar la sessión order

  messages.error(request, 'Orden cancelada')
  return redirect('index')

@login_required(login_url='login')
@validate_cart_and_order
def complete(request, cart, order):

  if request.user.id != order.user_id: # Si no es el mismo usuario quien creo la orden y quien la quiere cancelar.
    return redirect('carts:cart') # Retorna 'http://127.0.0.1:8000/carrito/'
  
  # Este metodo se crea en 'orders/models'
  order.complete()  # Modifica su estatus a COMPLETE

  thread = threading.Thread(target=Mail.send_complete_order, args=(
    order, request.user
  )) #En target se indica el motodo o función que queremos ejecutar en segundo plano
  thread.start()

  destroy_cart(request) # Elimina la sessión cart
  destroy_order(request)  # Eliminar la sessión order

  messages.success(request, 'Compra completada exitosamente')
  return redirect('index')




