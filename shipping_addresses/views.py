from django.shortcuts import render

from django.views.generic import ListView
from .models import ShippingAddress

from .forms import ShippingAddressForm

from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import UpdateView, DeleteView
from django.shortcuts import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order
from django.http import HttpResponseRedirect
# Create your views here.
class ShippingAddressListView(LoginRequiredMixin, ListView):
  login_url = 'login'
  model = ShippingAddress
  template_name = 'shipping_addresses/shipping_addresses.html'

  def get_queryset(self):
    return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
  login_url = 'login'
  model = ShippingAddress
  form_class = ShippingAddressForm
  template_name = 'shipping_addresses/update.html'
  success_message = 'Dirección actualizada exitosamente'

  def get_success_url(self):
    return reverse('shipping_addresses:shipping_addresses')
  
  def dispatch(self, request, *args, **kwargs):
    if request.user.id != self.get_object().user_id:
      return redirect('carts:cart')
  
    return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
  login_url = 'login'
  model = ShippingAddress
  template_name = 'shipping_addresses/delete.html'
  success_url = reverse_lazy('shipping_addresses:shipping_addresses')

  def dispatch(self, request, *args, **kwargs):
    if self.get_object().default:
      return redirect('shipping_addresses:shipping_addresses')
    
    if request.user.id != self.get_object().user_id:
      return redirect('carts:cart')

    # El metodo se define en shipping_addresses/models.py
    if self.get_object().has_orders():  # Sí el objecto shipping_address posee ordenes
      messages.error(request, 'La dirección esta asignada a una orden de compra.')
      return redirect('shipping_addresses:shipping_addresses')  # Retorna direcciones/

    return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
  form = ShippingAddressForm(request.POST or None)

  if request.method == 'POST' and form.is_valid():
    shipping_address = form.save(commit=False)
    shipping_address.user = request.user
    shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()
    
    shipping_address.save()

    if request.GET.get('next'): # Si la petición posee el parametro next
      if request.GET['next'] == reverse('orders:address'): # Si el valor de next es exactamente esa dirección, el usuario se encuentra en el proceso de orden de compra.
          # Se deben importar las funciones get_or_create_cart y order.
          cart = get_or_create_cart(request) # Obtiene el carrito de compras, Para poder obtener la orden de compra.
          order = get_or_create_order(cart, request) # Obtiene la orden.
          
          order.update_shipping_address(shipping_address)  # Establece la dirección recientemente creada a la orden de compra.
          return HttpResponseRedirect(request.GET['next']) # Para finalizar redirecciona al usuario a la sección dirección de la orden. Se importa el HttpResponseRedirect.

    messages.success(request, 'Dirección creada exitosamente')
    return redirect('shipping_addresses:shipping_addresses')

  return render(request, 'shipping_addresses/create.html', {
    'form': form
  })

@login_required(login_url='login')
def default(request, pk):
  shipping_address = get_object_or_404(ShippingAddress, pk=pk)

  if request.user.id != shipping_address.user_id:
    return redirect('carts:cart')
  
  #Obtener la antigua dirección principal y colocar default = False
  if request.user.has_shipping_address(): 
    request.user.shipping_address.update_default()

  shipping_address.update_default(True)

  return redirect('shipping_addresses:shipping_addresses')