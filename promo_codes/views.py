from django.shortcuts import render
from django.http import JsonResponse
from .models import PromoCode
from orders.decorators import validate_cart_and_order
from django.views.generic.list import ListView
# Create your views here.

@validate_cart_and_order
def validate(request, cart, order):
  code = request.GET.get('code')
  promo_code = PromoCode.objects.get_valid(code)

  if promo_code is None:
    return JsonResponse({
      'status': False
    }, status=404)

  order.apply_promo_code(promo_code)

  return JsonResponse({
    'status': True,
    'code': promo_code.code,
    'discount': promo_code.discount,
    'total': order.total
  })

class PromoCodesListView(ListView):
  template_name = 'promo_codes.html'
  queryset = PromoCode.objects.filter(used=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print(context)
    return context